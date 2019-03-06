import argparse

from .views import app


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--host', default='localhost', help='host')
    parser.add_argument('--port', default='5000', help='port')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True)
