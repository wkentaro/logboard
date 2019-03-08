import argparse

from .views import app


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--host', default='0.0.0.0', help='host')
    parser.add_argument('--port', default='5000', help='port')
    parser.add_argument('--debug', action='store_true', help='debug mode')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug)
