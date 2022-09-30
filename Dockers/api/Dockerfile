FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app app
COPY templates templates
COPY static static
COPY app.db .
COPY run.py .
COPY prod.sh .
COPY create_tables.py .
COPY load_fixtures.py .
COPY fixtures.json .
ENV FLASK_APP=run.py
ENV FLASK_ENV='production'
ENV FLASK_RUN_PORT=25000
COPY migrations migrations
ENV DATABASE_USER=hw_pg
ENV DATABASE_PASSWORD=hw_pg_password
ENV DATABASE_HOST=hw_pg_host
ENV DATABASE_PORT=5432
ENV DATABASE_NAME=hw_db

# CMD tail -f /dev/null
# CMD flask run -h 0.0.0.0 -p 8080
CMD bash ./prod.sh
