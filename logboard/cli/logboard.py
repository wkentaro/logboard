import argparse
import contextlib
import os
import socket
import sys

from ..views import app


@contextlib.contextmanager
def redirect_to_devnull(stdout=True, stderr=False):
    with open(os.devnull, 'w') as f:
        if stdout:
            sys.stdout = f
        if stderr:
            sys.stderr = f
        yield
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--logdir', default='logs', help='logs dir')
    parser.add_argument('--host', default='0.0.0.0', help='host')
    parser.add_argument('--port', default=None, help='port')
    parser.add_argument('--debug', action='store_true', help='debug mode')
    parser.add_argument(
        '--filter', '-f', nargs='+', default=[], help='filter keys'
    )
    args = parser.parse_args()

    app.config['logdir'] = args.logdir
    app.config['filter'] = args.filter

    os.environ['FLASK_ENV'] = 'development'

    print(' * Log directory: {}'.format(args.logdir))

    if args.port:
        app.run(host=args.host, port=args.port, debug=args.debug)
    else:
        for port in range(7006, 9999):
            try:
                with redirect_to_devnull():
                    app.run(host=args.host, port=port, debug=args.debug)
                    break
            except socket.error:
                pass
