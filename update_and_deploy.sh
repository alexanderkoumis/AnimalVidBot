#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]; then
    # Get script dir on Mac
    AVB_DIR=$(dirname "$(stat -f "$0")")
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Get script dir on Linux
    AVB_DIR=$(dirname "$(readlink -f "$0")")
fi

OLD_DIR=$PWD
cd $AVB_DIR
git reset --hard HEAD
git pull
pkill -9 -f AnimalVidBot/app.py
python3 -u $AVB_DIR/app.py $AVB_DIR/config.json | tee -a $AVB_DIR/stdout.log &
disown
cd $OLD_DIR
