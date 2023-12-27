FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

COPY requirements.txt /temp/requirements.txt
COPY . /service
WORKDIR /service


RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

RUN chown -R service-user:service-user /service && chmod 755 /service

USER service-user

