#!/bin/bash

echo_bold () {
  echo -e "\033[1m$*\033[0m"
}

echo_bold "==> Running Terminal Example (logtable)"
logtable --logdir logs

echo_bold "==> Running Browser Example (logbrowser)"
logboard --logdir logs
