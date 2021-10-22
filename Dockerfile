FROM 018008741390.dkr.ecr.us-east-2.amazonaws.com/uwsgi-nginx-flask

ENV PYTHONPATH=.

RUN mkdir -p /app

WORKDIR /app

COPY /main.py /app
COPY /default_timeout.conf /app
COPY /uwsgi.ini /app
COPY /requirements /app/requirements
COPY requirements.txt /app
COPY application.py /app
COPY /app /app/app

# install system dependencies
RUN   cp default_timeout.conf /etc/nginx/default_timeout.conf \
  && apt-get update \
  && apt-get -y install nginx \
  && apt-get clean

RUN pip3 install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 5000
VOLUME [ "/app" ]
