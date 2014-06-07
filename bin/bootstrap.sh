#!/bin/bash
#author: tim.tang
#aim: Auto start cogenda web server.

set -e

cd /home/root/apps/cogenda-web
./setenv.sh
source venv/bin/activate

PID_FILE="/tmp/cogenda-app.pid"

if [ -f $PID_FILE ]; then
    cat $PID_FILE | xargs kill -9 
fi

make run-prod
