#!/bin/sh

export DJANGO_SETTINGS_MODULE="drp49.settings"

gunicorn "drp49.wsgi:application" \
--name="drp49_server" \
--workers=1 \
--bind="unix:/tmp/drp49.sock" \
--log-level="info" \
--log-file="gunicorn.log" \
--daemon
