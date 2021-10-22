#!/bin/bash

echo "================================================="
echo "Starting lamconnect microservice"
echo "================================================="

export FLASK_DEBUG=0
export FLASK_APP=application.py
export PYDEVD_WARN_EVALUATION_TIMEOUT=500
# flask run -h '0.0.0.0' -p 5000
