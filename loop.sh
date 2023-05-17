#!/usr/bin/env bash
while [[ 1 == 1 ]];
do
    echo "`date`: Loop"
    git fetch
    git pull
    source venv/bin/activate
    source myenv
    python download.py
    python unpack.py
    python createspecfiles.py
    
    sleep 10
done
