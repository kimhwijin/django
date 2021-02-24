# pull official base image
FROM python:3.7.4-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# set environment variables, variables have real value in core/settings.py
# 장고 whitelist, allowed host, cors 관련 설정 (변수 형태로 들어감), settings.py와 매핑
ENV DJANGO_ALLOWED_HOSTS $DJANGO_ALLOWED_HOSTS
ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY
ENV DJANGO_CORS_ORIGIN_WHITELIST $DJANGO_CORS_ORIGIN_WHITELIST

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

# mysql 설치
#RUN apk update
#RUN apk add --update mysql mysql-client && rm -f /var/cache/apk/*

# numpy, pandas 설치
RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install bottle numpy cython pandas

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
Run pip install mysqlclient-2.0.3.tar.gz
RUN pip install -r requirements.txt