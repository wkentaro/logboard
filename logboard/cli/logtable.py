# flake8: noqa

import argparse
import os.path as osp

import tabulate

from ..config import get_config
from ..parser import parse


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--logdir', default='logs', help='logs dir')
    parser.add_argument('--hide', nargs='+', default=[], help='hide keys')
    args = parser.parse_args()

    config = get_config()
    root_dir = osp.abspath(args.logdir)
    df, summary_keys, args_keys, log_keys = parse(config, root_dir)

    print(' * Log directory: {}'.format(args.logdir))

    summary_keys = ['log_dir'] + summary_keys

    headers = []
    for key in summary_keys:
        if key in args.hide:
            continue
        if key in args_keys:
            headers.append(key)
        elif key in log_keys:
            headers.append(key)
            headers.append('')
        else:
            headers.append(key)

    for i, header in enumerate(headers):
        headers[i] = header.replace('/', '/\n')

    rows = []
    for index, df_row in df[summary_keys].iterrows():
        row = []
        for key, x in zip(summary_keys, df_row):
            if key in args.hide:
                continue
            if isinstance(x, tuple):
                assert len(x) == 2
                row.append(x[0])
                row.append(x[1])
            else:
                row.append(x)
        rows.append(row)

    table = tabulate.tabulate(
        tabular_data=rows,
        headers=headers,
        tablefmt='grid',
        stralign='center',
        showindex=True,
        disable_numparse=True,
    )
    print(table)
