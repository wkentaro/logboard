# flake8: noqa

import argparse
import os.path as osp
import re
import sys
import warnings

import tabulate

from ..parser import parse


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--logdir', default='logs', help='logs dir')
    parser.add_argument(
        '--filter', '-f', nargs='+', default=[], help='filter keys'
    )
    parser.add_argument('--keys', action='store_true')
    args = parser.parse_args()

    root_dir = osp.abspath(args.logdir)
    df, summary_keys, _, _ = parse(root_dir)

    print(' * Log directory: {}'.format(args.logdir))

    summary_keys = ['log_dir'] + summary_keys

    summary_keys_ = []
    for key in summary_keys:
        for pattern in args.filter:
            if re.match(pattern, key):
                break
        else:
            summary_keys_.append(key)
    summary_keys = summary_keys_

    if args.keys:
        for key in summary_keys:
            print(key)
        sys.exit(0)

    headers = summary_keys[:]
    for i, header in enumerate(headers):
        headers[i] = header.replace('/', '/\n')

    if df.empty:
        df.columns = summary_keys

    rows = []
    for index, df_row in df[summary_keys].iterrows():
        row = []
        for key, x in zip(summary_keys, df_row):
            if isinstance(x, tuple):
                assert len(x) == 2
                row.append('{}\n{}'.format(*x))
            else:
                row.append(x)
        rows.append(row)

    table = tabulate.tabulate(
        tabular_data=rows,
        headers=headers,
        tablefmt='fancy_grid',
        stralign='center',
        showindex=True,
        disable_numparse=True,
    )
    print(table)
