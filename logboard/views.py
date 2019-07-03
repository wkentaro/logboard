import datetime
import os.path as osp
import re

import flask

from .parser import parse


app = flask.Flask('logboard')


@app.route('/')
def index():
    root_dir = osp.abspath(app.config['logdir'])
    df, summary_keys, args_keys, log_keys = parse(root_dir)

    summary_keys_ = []
    for key in summary_keys:
        for pattern in app.config['filter']:
            if re.match(pattern, key):
                break
        else:
            summary_keys_.append(key)
    summary_keys = summary_keys_

    if 'log_dir' in flask.request.args and \
            flask.request.args['log_dir'] not in df.log_dir.values:
        request_args = dict(flask.request.args)
        request_args.pop('log_dir')
        return flask.redirect(flask.url_for('index', **request_args))

    return flask.render_template(
        'index.html',
        timestamp=datetime.datetime.now(),
        root_dir=root_dir,
        summary_df=df,
        summary_keys=summary_keys,
        args_keys=args_keys,
        log_keys=log_keys,
    )


@app.route('/logs/<log_dir>/<path:filename>')
def logs(log_dir, filename):
    root_dir = osp.abspath(app.config['logdir'])
    return flask.send_from_directory(osp.join(root_dir, log_dir), filename)
