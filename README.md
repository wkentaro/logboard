<h1 align="center">
  logboard
</h1>

<h4 align="center">
  Monitor and Compare Logs on Browser/Terminal.
</h4>

<div align="center">
  <a href="https://travis-ci.com/wkentaro/logboard">
    <img src="https://travis-ci.com/wkentaro/logboard.svg?token=zM5rExyvuRoJThsnqHAF&branch=master">
  </a>

  <br/>

  <img src=".readme/browser.png" width="60%">
  <img src=".readme/terminal.png" width="60%" />
</div>


## Description

Inspired by [tensorboard](https://github.com/tensorflow/tensorboard),
[grip](https://github.com/joeyespo/grip) and [notable](https://github.com/notable/notable),
all of which serve light-weight GUI by

- only using static files (e.g., markdown files without DB);
- single command (e.g., `tensorboard --logdir logs/` and `grip README.md`).


## Why not `tensorboard`?

I also use `tensorboard` in addition to this tool.
But currently `tensorboard` doesn't support comparing different configurations
for each log (e.g., git-hash of the code, learning rate, training strategy).
`logboard` is a kind of extra plugin to `tensorboard`
(but you need to run in different terminal, unfortunately).
I expect this kind of feature will be included in `tensorboard` in the future.


## Usage

### Browser (`logboard`)

```bash
$ cd examples

$ cat .logboard
[logboard]
-summary=out,timestamp,loglevel,gpu,seed,lr .*,.*main/loss.*(max)

$ cat logs/20190310_093252.724597/args
{
    "loglevel": "info",
    "gpu": 0,
    "seed": 0,
    "class_ids": [
        1
    ],
    "lr": 0.001,
    "timestamp": "2019-03-10T09:32:52.724597",
    "out": "/home/wkentaro/logboard/examples/logs/20190310_093252.724597",
    "hostname": "computer1",
    "githash": "b48ce48"
}

$ logboard --logdir logs/  # like tensorboard --logdir logs/
```


### Terminal (`logtable`)

```bash
$ cd examples

$ logtable --hide updated_at epoch hostname class_ids 'main/loss_quaternion (min)' 'main/loss_translation (min)' 'validation/main/loss_quaternion (min)' 'validation/main/loss_translation (min)'
 * Log directory: logs
+----+------------------------+-------------+----------------+-----------+-------+--------------+-----------+---------------+----------+
|    |        log_dir         |  iteration  |  elapsed_time  |  githash  |  lr   |    main/     |           |  validation/  |          |
|    |                        |             |                |           |       |  loss (min)  |           |     main/     |          |
|    |                        |             |                |           |       |              |           |  loss (min)   |          |
+====+========================+=============+================+===========+=======+==============+===========+===============+==========+
| 0  | 20190310_093252.724597 |    1740     |    1:47:02     |  b48ce48  | 0.001 |    0.0088    | (1, 1580) |     0.18      | (0, 880) |
+----+------------------------+-------------+----------------+-----------+-------+--------------+-----------+---------------+----------+
| 1  | 20190310_093829.691289 |    1720     |    1:45:37     |  f766b97  | 0.001 |    0.012     | (1, 1620) |     0.19      | (0, 440) |
+----+------------------------+-------------+----------------+-----------+-------+--------------+-----------+---------------+----------+
```
