#!/usr/bin/env python3

import connexion

from drm_appointment import database, encoder
import os

app = connexion.App(__name__, specification_dir="./openapi/")
app.app.json_encoder = encoder.JSONEncoder
app.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL", "sqlite:///:memory:")
app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database.db.init_app(app.app)

if app.app.config["ENV"] == "development":
    with app.app.app_context():
        database.db.create_all()

app.add_api("openapi.yaml", arguments={"title": "DR Manager - Appointment API"}, pythonic_params=True)
