#!/bin/bash

echo_bold () {
  echo -e "\033[1m$*\033[0m"
}

echo_bold "==> Running Terminal Example (logtable)"
logtable --logdir logs --filter out timestamp loglevel gpu seed 'lr .*' '.*main/loss.*(max)' '.*loss_.*'

echo_bold "==> Running Browser Example (logbrowser)"
logboard --logdir logs --filter out timestamp loglevel gpu seed 'lr .*' '.*main/loss.*(max)' '.*loss_.*'
