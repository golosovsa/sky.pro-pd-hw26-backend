FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app app
COPY templates templates
COPY static static
COPY run.py .
COPY prod.sh .
COPY create_tables.py .
COPY drop_tables.py .
COPY load_fixtures.py .
COPY fixtures.json .
COPY migrations migrations

CMD gunicorn -w 4 -b 0.0.0.0:3000 run:app