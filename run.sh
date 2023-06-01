#!/bin/sh

# Set environment variables first.
# See `drp49_secret.txt`.

# Create working directory
DIR="/tmp/drp49"
mkdir -p "$DIR"

# Kill old process if still running
if [ -e "$DIR/gunicorn.pid" ]
then
  kill `cat $DIR/gunicorn.pid`
fi

# Start `gunicorn` in daemon mode
export DJANGO_SETTINGS_MODULE="drp49.settings"

gunicorn "drp49.wsgi:application" \
--name="drp49_server" \
--workers=1 \
--pid="$DIR/gunicorn.pid" \
--bind="unix:$DIR/gunicorn.sock" \
--log-level="info" \
--log-file="$DIR/gunicorn.log" \
--daemon
