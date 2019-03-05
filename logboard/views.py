try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
import datetime
import json
import os
import os.path as osp

import flask


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
    root_dir = osp.abspath('logs')
    log_dirs = sorted(os.listdir(root_dir))

    # static folder
    app.config['STATIC_FOLDER'] = root_dir

    # config
    config = get_config()

    # params
    args_keys = set()
    args_data = {}
    for log_dir in log_dirs:
        args_file = osp.join(root_dir, log_dir, 'args')
        with open(args_file) as f:
            args = json.load(f)
        args_keys = set(args.keys()) | args_keys
        args_data[log_dir] = args

    if 'log_dir' in flask.request.args and \
            flask.request.args['log_dir'] not in args_data:
        request_args = dict(flask.request.args)
        request_args.pop('log_dir')
        return flask.redirect(flask.url_for('index', **request_args))

    args_keys = args_keys ^ config['-summary']

    return flask.render_template(
        'index.html',
        timestamp=datetime.datetime.now(),
        root_dir=root_dir,
        log_dirs=log_dirs,
        args_keys=sorted(args_keys),
        args_data=args_data,
        figures=config['figure'],
    )


@app.route('/logs/<log_dir>/<path:filename>')
def logs(log_dir, filename):
    root_dir = osp.abspath('logs')
    return flask.send_from_directory(osp.join(root_dir, log_dir), filename)
