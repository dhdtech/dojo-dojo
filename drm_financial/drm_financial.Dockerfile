FROM tiangolo/uwsgi-nginx-flask:latest 

ENV PYTHONPATH=.

RUN mkdir -p /app

WORKDIR /app

COPY /requirements /app/requirements
COPY /drm_appointment /app/drm_financial

# install system dependencies
RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get -y install nginx \
  && apt-get -y install -y postgresql-client \
  && apt-get clean \
  && pip3 install --no-cache-dir -r requirements/base.txt \
  && apt-get update \
  && rm -rf /var/lib/apt/lists/*

EXPOSE 5000
VOLUME [ "/app" ]
