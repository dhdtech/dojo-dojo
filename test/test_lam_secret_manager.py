import json
import os
from unittest import TestCase, mock

from app.secret_manager.secret import get_secret


class TestSecretManager(TestCase):
    """Tests for secret_manager"""

    def test_get_secret(self):
        with mock.patch.dict(os.environ, {"AWS_ACCESS_KEY_ID": ""}):
            with mock.patch("logging.Logger.warning") as logger_warning_mock:
                get_secret("secret_name")
                logger_warning_mock.assert_called_with(
                    "SKF LAM: Couldn`t find AWS credentials. Are you missing export env variables?"
                )

        with mock.patch("boto3.session.Session.client") as get_secret_value_mock:
            with mock.patch("base64.b64decode") as base64_mock:
                base64_mock.return_value = """{"SecretString": "string"}"""

                response = get_secret()
                self.assertEqual(response, {"SecretString": "string"})

        class MockedClass:
            def get_secret_value(self, SecretId=None):
                return {"SecretString": """{"teste":"string"}"""}

        with mock.patch("boto3.session.Session.client") as get_secret_value_mock:
            get_secret_value_mock.return_value = MockedClass()
            response = get_secret("teste")
            self.assertEqual(response, "string")
