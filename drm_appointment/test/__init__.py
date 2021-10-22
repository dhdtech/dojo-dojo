import logging
import os

import connexion
from flask_testing import TestCase

from drm_appointment.encoder import JSONEncoder
import drm_appointment.database as database


class BaseTestCase(TestCase):
    def create_app(self):

        os.environ["FLASK_ENV"] = "development"

        logging.getLogger("connexion.operation").setLevel("ERROR")
        app = connexion.App(__name__, specification_dir="../openapi/")
        app.app.json_encoder = JSONEncoder

        # Initializing database
        app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        database.db.init_app(app.app)
        with app.app.app_context():
            database.db.create_all()

        app.add_api("openapi.yaml", pythonic_params=True)
        return app.app
