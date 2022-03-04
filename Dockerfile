FROM python:3.8-alpine
MAINTAINER Pablo De Maio Marchetti

ENV PYTHONUNBUFFERED 1
ENV PATH="/home/user/.local/bin:$PATH"
RUN mkdir /app

WORKDIR /app
COPY ./app /app

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN adduser -D user
RUN chown -R user:user /app

RUN apk del .tmp-build-deps

USER user