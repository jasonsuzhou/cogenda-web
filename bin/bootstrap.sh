#!/bin/bash
#author: tim.tang
#aim: Auto start cogenda web server.

set -e

cd /home/root/apps/cogenda-web
./setenv.sh
source venv/bin/activate
make run
