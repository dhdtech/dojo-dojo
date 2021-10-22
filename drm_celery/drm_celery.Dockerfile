FROM python:3.9-alpine

ENV C_FORCE_ROOT true

COPY /drm_celery /queue
WORKDIR /queue

RUN pip install -U setuptools pip
RUN pip install -r requirements.txt

# hot code reloading
CMD watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A tasks worker --concurrency=1 --loglevel=INFO -E