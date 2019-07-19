import datetime
import json
import os
import os.path as osp

import pandas


def parse(root_dir, **kwargs):
    """parse(root_dir, sort=None, q=None)

    Parse log directory to create a log table.

    Parameters
    ----------
    root_dir: str
        Root directory that contains logs.
    sort: str, optional
        Sort logs.
    q: str, optional
        Query of log keys.
    float_format: str, optional.
        Float value formatting (default: '{:.3g}').

    Returns
    -------
    df: pandas.DataFrame
        Log table.
    summary_keys: list of str
        List of keys from summary.
    args_keys: list of str
        List of keys from args.
    log_keys: list of str
        List of keys from log.
    """

    sort = kwargs.get('sort', None)
    q = kwargs.get('q', None)
    float_format = kwargs.get('float_format', '{:.3g}')

    log_dirs = sorted(os.listdir(root_dir))

    # params
    args_keys = set()
    log_keys = set()
    data = []
    for log_dir in sorted(log_dirs):
        args_file = osp.join(root_dir, log_dir, 'args')
        try:
            with open(args_file) as f:
                args = json.load(f)
        except IOError:
            continue
        args_keys = args_keys | set(args.keys())
        datum = args
        datum['log_dir'] = log_dir

        log_file = osp.join(root_dir, log_dir, 'log')
        try:
            with open(log_file) as f:
                log = json.load(f)
        except IOError:
            data.append(datum)
            continue

        log = pandas.DataFrame(data=log)
        datum['epoch'] = log['epoch'].max()
        datum['iteration'] = log['iteration'].max()
        datum['elapsed_time'] = \
            datetime.timedelta(seconds=int(round(log['elapsed_time'].max())))

        now = datetime.datetime.now()
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
        seconds = (now - mtime).total_seconds()
        datum['updated_at'] = datetime.timedelta(seconds=int(round(seconds)))

        for col in log.columns:
            if col in ['epoch', 'iteration', 'elapsed_time']:
                continue

            key = '{} (max)'.format(col)
            log_keys.add(key)
            index = log[col].idxmax()
            datum[key] = (
                log[col][index], (log['epoch'][index], log['iteration'][index])
            )

            key = '{} (min)'.format(col)
            log_keys.add(key)
            index = log[col].idxmin()
            datum[key] = (
                log[col][index], (log['epoch'][index], log['iteration'][index])
            )

        data.append(datum)

    summary_keys = ['epoch', 'iteration', 'elapsed_time', 'updated_at']
    summary_keys += sorted(args_keys)
    summary_keys += sorted(log_keys)

    df = pandas.DataFrame(data=data, columns=['log_dir'] + summary_keys)

    if sort is not None:
        key = sort
        ascending = True
        if key.startswith('-'):
            key = key[1:]
            ascending = False
        df = df.sort_values(by=key, ascending=ascending)

    # format
    for col in df.columns:
        if col.endswith(' (min)') or col.endswith(' (max)'):
            key = col[:-6]
            values = []
            for value in df[col].values:
                if isinstance(value, tuple):
                    values.append((
                        float_format.format(value[0]),
                        value[1],
                    ))
                else:
                    values.append((value, (float('nan'), float('nan'))))
            df[col] = values
        elif df[col].dtype.name == 'timedelta64[ns]':
            values = []
            for value in df[col]:
                try:
                    value = datetime.timedelta(seconds=value.total_seconds())
                    value = str(value)
                except ValueError:
                    pass
                values.append(value)
            df[col] = values
        else:
            df[col] = df[col].astype(str)

    if q is not None:
        try:
            df = df.query(q)
        except Exception:
            pass

    return df, summary_keys, args_keys, log_keys
