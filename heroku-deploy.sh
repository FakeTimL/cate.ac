#!/usr/bin/sh

cd backend

# Compile translations
django-admin compilemessages

# Initialise static files
python manage.py collectstatic

# Update database
python manage.py migrate
