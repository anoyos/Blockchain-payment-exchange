#!/bin/bash

. venv/bin/activate
. deploy/set_env

uwsgi \
 --module=wsgi:app \
 --master \
 --http-socket=0.0.0.0:5007 \
 --socket=0.0.0.0:6007 \
 --max-requests=50000 \
 --vacuum \
 --harakiri=45 \
 --enable-threads \
 --threads=25 \
 --processes=1 \
 --pidfile=logs/pid.pid \
 --touch-reload=./touchme 
