# flake8: noqa

import argparse
import os.path as osp
import re
import sys
import textwrap
import warnings

import tabulate

from ..parser import parse


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--logdir',
        '-l',
        default='logs',
        help='logs dir',
    )
    parser.add_argument(
        '--filter',
        '-f',
        nargs='+',
        default=[],
        help='filter keys',
    )
    parser.add_argument('--keys', action='store_true')
    parser.add_argument(
        '--significant-figures',
        '-s',
        type=int,
        default=3,
        help='significant figures',
    )
    parser.add_argument(
        '--index',
        '-i',
        type=int,
        nargs='+',
        help='index filtering',
    )
    parser.add_argument(
        '--column',
        '-c',
        type=int,
        default=30,
        help='maximum column width (0 for infinite)',
    )
    parser.add_argument(
        '--multi-column',
        action='store_true',
        help='prefer multi-column to vertically shorten the table',
    )
    args = parser.parse_args()

    float_format = '{:.%dg}' % args.significant_figures

    root_dir = osp.abspath(args.logdir)
    df, summary_keys, _, log_keys = parse(root_dir, float_format=float_format)

    if args.index is not None:
        df = df.ix[args.index]

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

    headers = ['']
    for key in summary_keys:
        key_short = key.replace('/', '/\n')
        headers.append(key_short)
        if args.multi_column and key in log_keys:
            headers.append('')

    if df.empty:
        df.columns = summary_keys

    rows = []
    for index, df_row in df[summary_keys].iterrows():
        row = [index]
        for key, x in zip(summary_keys, df_row):
            if isinstance(x, tuple):
                assert len(x) == 2
                if args.multi_column:
                    row.extend(x)
                else:
                    x = '\n'.join(str(xi) for xi in x)
                    row.append(x)
            else:
                x = str(x)
                x = textwrap.wrap(x, width=args.column) if args.column else [x]
                x = '\n'.join(x)
                row.append(x)
        rows.append(row)

    table = tabulate.tabulate(
        tabular_data=rows,
        headers=headers,
        tablefmt='fancy_grid',
        stralign='center',
        showindex=False,
        disable_numparse=True,
    )
    print(table)
