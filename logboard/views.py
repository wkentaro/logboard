try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
import datetime
import json
import os
import os.path as osp
import re

import flask
import pandas


app = flask.Flask(__name__)


def get_config():
    config = {
        '-summary': set(),
        'figure': ['loss.png'],
    }

    parser = ConfigParser()
    parser.read('.chainerlg')

    section = parser['chainerlg']

    try:
        config['-summary'] = set(filter(None, section['-summary'].split(',')))
    except KeyError:
        pass

    try:
        config['figure'] = filter(None, section['figure'].split(','))
    except KeyError:
        pass

    return config


@app.route('/')
def index():
    root_dir = osp.abspath(app.config['logdir'])
    log_dirs = sorted(os.listdir(root_dir))

    # static folder
    app.config['STATIC_FOLDER'] = root_dir

    # config
    config = get_config()

    # params
    summary_keys = ['epoch', 'iteration', 'elapsed_time']
    args_keys = []
    data = []
    for log_dir in sorted(log_dirs):
        args_file = osp.join(root_dir, log_dir, 'args')
        try:
            with open(args_file) as f:
                args = json.load(f)
        except IOError:
            continue
        for key in args:
            if key not in summary_keys:
                summary_keys.append(key)
                args_keys.append(key)
        datum = args
        datum['log_dir'] = log_dir

        log_file = osp.join(root_dir, log_dir, 'log')
        try:
            with open(log_file) as f:
                log = json.load(f)
        except IOError:
            data.append(datum)
            continue

        log = pandas.DataFrame(data=log)
        datum['epoch'] = log['epoch'].max()
        datum['iteration'] = log['iteration'].max()
        datum['elapsed_time'] = \
            datetime.timedelta(seconds=int(round(log['elapsed_time'].max())))

        for col in log.columns:
            if col in ['epoch', 'iteration', 'elapsed_time']:
                continue

            key = '{} (max)'.format(col)
            if key not in summary_keys:
                summary_keys.append(key)
            index = log[col].idxmax()
            datum[key] = (
                '{:.4g}'.format(log[col][index]),
                log['iteration'][index]
            )

            key = '{} (min)'.format(col)
            if key not in summary_keys:
                summary_keys.append(key)
            index = log[col].idxmin()
            datum[key] = (
                '{:.4g}'.format(log[col][index]),
                log['iteration'][index]
            )

        for key, value in list(datum.items()):
            if not isinstance(value, tuple):
                datum[key] = str(value)
        data.append(datum)

    df = pandas.DataFrame(data=data)
    if 'q' in flask.request.args:
        try:
            df = df.query(flask.request.args['q'])
        except Exception:
            pass

    if 'log_dir' in flask.request.args and \
            flask.request.args['log_dir'] not in df.log_dir.values:
        request_args = dict(flask.request.args)
        request_args.pop('log_dir')
        return flask.redirect(flask.url_for('index', **request_args))

    for pattern in config['-summary']:
        for key in summary_keys[:]:
            if re.match(pattern, key):
                summary_keys.remove(key)

    return flask.render_template(
        'index.html',
        timestamp=datetime.datetime.now(),
        root_dir=root_dir,
        summary_df=df,
        summary_keys=summary_keys,
        args_keys=args_keys,
        figures=config['figure'],
    )


@app.route('/logs/<log_dir>/<path:filename>')
def logs(log_dir, filename):
    root_dir = osp.abspath(app.config['logdir'])
    return flask.send_from_directory(osp.join(root_dir, log_dir), filename)
