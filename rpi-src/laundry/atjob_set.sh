#!/bin/bash

if [ $# -ne 2 ]; then
  echo "指定された引数は$#個です。" 1>&2
  exit 1
fi

time=$1
date=$2

at $time $date -f servo_start.sh