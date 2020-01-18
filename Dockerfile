FROM python:3
ENV PYTHONBUFFERED 1
WORKDIR /code
RUN pip install django psycopg2 Pillow celery janome pandas numpy
COPY ./textstats /code