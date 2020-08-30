#!/bin/bash

NUM_WORKERS=3
TIMEOUT=200
PORT=$1

while true; do

    flask db init --multidb --directory /app_dir/db/migrations
    flask db migrate --directory /app_dir/db/migrations
    flask db upgrade --directory /app_dir/db/migrations

    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done

exec gunicorn wsgi:app \
--bind 0.0.0.0:$PORT \
--workers $NUM_WORKERS \
--timeout $TIMEOUT
