#! /bin/sh
export FLASK_APP=webapp
flask db migrate -m "Добавил форму"
flask db upgrade