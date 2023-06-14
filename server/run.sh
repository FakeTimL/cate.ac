#!/bin/sh

# Set environment variables first.
# See `drp49_secret.txt`.

# Create working directory
DIR="/tmp/drp49"
mkdir -p "$DIR"

# Kill old process if still running
if [ -e "$DIR/gunicorn.pid" ]
then
  PID=`cat $DIR/gunicorn.pid`
  kill $PID

  # Wait until old process stops
  # See: https://stackoverflow.com/a/29281720
  while kill -0 $PID
  do
    echo "Waiting for old server process to stop..."
    sleep 1
  done
fi

# Wait until socket is no longer used
while [ -e "$DIR/gunicorn.sock" ]
do
  echo "Waiting for socket file to become available..."
  sleep 1
done

echo "Starting server..."

# Start `gunicorn` in daemon mode
export DJANGO_SETTINGS_MODULE="config.config"

gunicorn "config.wsgi:application" \
--name="drp49_server" \
--workers=1 \
--pid="$DIR/gunicorn.pid" \
--bind="unix:$DIR/gunicorn.sock" \
--log-level="info" \
--log-file="$DIR/gunicorn.log" \
--daemon

echo "Gunicorn server started. Log file is at \"$DIR/gunicorn.log\"."
