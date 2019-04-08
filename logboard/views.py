import datetime
import os.path as osp

import flask

from .config import get_config
from .parser import parse


app = flask.Flask('logboard')


@app.route('/')
def index():
    config = get_config()
    root_dir = osp.abspath(app.config['logdir'])
    df, summary_keys, args_keys, log_keys = parse(config, root_dir)

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
