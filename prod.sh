#!/bin/bash

gunicorn -w 4 -b 0.0.0.0:25000 run:app &
sleep 5
flask db upgrade
python3 create_tables.py
python3 load_fixtures.py
tail -f /dev/null