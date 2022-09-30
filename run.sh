#!/bin/bash

source venv/bin/activate
export FLASK_APP=run.py
export FLASK_ENV='development'
export FLASK_RUN_PORT=25000

if [ $# -gt 0 ]; then

  if [[ $1 =~ "d" ]]; then
    echo "Drop tables"
    python3 ./drop_tables.py
  fi

  if [[ $1 =~ "c" ]]; then
    echo "Create tables"
    python3 ./create_tables.py
  fi

  if [[ $1 =~ "l" ]]; then
    echo "Load fixtures"
    python3 ./load_fixtures.py
  fi

  if [[ $1 =~ "r" ]]; then
    echo "Start app"
    flask run
  fi

    if [[ $1 =~ "m" ]]; then
    echo "Init db migrates"
    rm -fr ./migrations
    flask db init
    flask db migrate -m "Initial migration"
  fi

  if [[ $1 =~ "h" ]]; then
    echo "./run.sh      - Run app"
    echo "./run.sh d    - Drop tables"
    echo "./run.sh c    - Create tables"
    echo "./run.sh l    - Load fixtures"
    echo "./run.sh r    - Run app"
    echo "You can combine params:"
    echo "./run.sh dclr  - Drop tables, cechoreate tables, load fixtures and run app"
  fi

else
  flask run
fi