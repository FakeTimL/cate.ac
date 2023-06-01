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

# Wait until socket is no longer used
while [ -e "$DIR/gunicorn.sock" ]
do
  echo "Waiting for socket..."
  sleep 1
done

# Start `gunicorn` in daemon mode
export DJANGO_SETTINGS_MODULE="config.settings"

gunicorn "config.wsgi:application" \
--name="drp49_server" \
--workers=1 \
--pid="$DIR/gunicorn.pid" \
--bind="unix:$DIR/gunicorn.sock" \
--log-level="info" \
--log-file="$DIR/gunicorn.log" \
--daemon
