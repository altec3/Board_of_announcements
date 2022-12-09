#!/bin/bash
python manage.py loaddata users.json
python manage.py loaddata ads.json
python manage.py loaddata comments.json
exec "$@"
