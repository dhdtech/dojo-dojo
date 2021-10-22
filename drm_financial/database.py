"""Setup for the database."""

import os

from flask_sqlalchemy import SQLAlchemy

from open_alchemy import init_yaml

# Construct models
db = SQLAlchemy()
SPEC_DIR = os.path.dirname(__file__)
SPEC_FILE = os.path.join(SPEC_DIR, "openapi/openapi.yaml")
MODELS_FILENAME = os.path.join(SPEC_DIR, "models/models_sqlalchemy.py")
init_yaml(SPEC_FILE, base=db.Model, models_filename=MODELS_FILENAME)
