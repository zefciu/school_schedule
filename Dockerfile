FROM python:3.13

RUN apt update
RUN apt install wait-for-it
RUN pip install -U pip


ADD . /school_schedule
WORKDIR /school_schedule

RUN pip install -r requirements.txt
# RUN python manage.py runserver
