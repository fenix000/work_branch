#! /bin/sh
export FLASK_APP=webapp
flask db migrate -m "Disable avatars"
flask db upgrade