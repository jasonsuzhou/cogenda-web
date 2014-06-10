#!/bin/bash
#author: tim.tang
#aim: Auto start cogenda web server.

set -e
COGENDA_WEB_PATH="/home/tim/apps/cogenda-web"
COGENDA_DB="/home/tim/apps/cogenda-web/migration/cogenda-app.db"

# stop cogenda application.
PID_FILE="/tmp/cogenda-app.pid"
if [ -f $PID_FILE ]; then
    ps -ef | grep 'cogenda-app' | grep -v "grep" | awk '{print $2}' | xargs kill
    #cat $PID_FILE | xargs kill -9
fi

cd $COGENDA_WEB_PATH
./setenv.sh
source venv/bin/activate
if [ -f $COGENDA_DB ]; then
    make db-migrate  
else
    make db-init
fi
make run-prod
