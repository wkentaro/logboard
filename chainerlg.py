import os
import os.path as osp

import flask
import yaml


app = flask.Flask(__name__)


@app.route('/')
def index():
    root_dir = osp.abspath('logs')
    log_dirs = os.listdir(root_dir)

    app.config['STATIC_FOLDER'] = root_dir

    params_keys = set()
    params_data = {}
    for log_dir in log_dirs:
        params_file = osp.join(root_dir, log_dir, 'params.yaml')
        with open(params_file) as f:
            params = yaml.load(f)
        params_keys = set(params.keys()) | params_keys
        params_data[log_dir] = params

    return flask.render_template(
        'index.html',
        root_dir=root_dir,
        log_dirs=log_dirs,
        params_keys=params_keys,
        params_data=params_data,
    )


@app.route('/logs/<log_dir>/<path:filename>')
def logs(log_dir, filename):
    root_dir = osp.abspath('logs')
    return flask.send_from_directory(osp.join(root_dir, log_dir), filename)


def main():
    app.run(debug=True)
