#! /bin/sh
export FLASK_APP=webapp
flask db migrate -m "Изменил форму Документации"
flask db upgrade