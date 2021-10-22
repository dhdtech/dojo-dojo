import requests_mock
from unittest import TestCase, mock
from app.lamconnect.lamconnect import SITE_NAME


class TestLamConnect(TestCase):
    """Tests for lamconnect.lamconnect"""

    @requests_mock.mock()
    def test__proxy_get(self, m):
        from app.lamconnect.lamconnect import app

        app.testing = True

        with app.test_client() as client:
            m.register_uri("GET", SITE_NAME, text="")
            response_code = client.get("/")._status_code
            self.assertEqual(response_code, 200)

    @requests_mock.mock()
    def test__proxy_post(self, m):
        from app.lamconnect.lamconnect import app

        app.testing = True

        with app.test_client() as client:
            m.register_uri("POST", SITE_NAME + "test", text="")
            response_code = client.post("/test", json={})._status_code
            self.assertEqual(response_code, 200)

    # def test_get_from_secret_manager(self):
    #     class MockedClass:
    #         def get_secret_value(self, SecretId=None):
    #             return {"SecretString": """{"teste":"string"}"""}

    #     with mock.patch("boto3.session.Session.client") as get_secret_value_mock:
    #         get_secret_value_mock.return_value = MockedClass()
    #         response = AWS.get_from_secret_manager(self, key_name="teste")
    #         self.assertEqual(response, "string")

    # def test_orderbook_by_customer_id_and_operational_unit_id(self):
    #     with mock.patch("app.lamconnect.lamconnect.get_generic_query") as get_generic_query_mock:
    #         with mock.patch("app.lamconnect.lamconnect.AWS.get_from_secret_manager") as get_secret_mock:
    #             get_secret_mock.return_value = "123456"
    #             get_generic_query_mock.return_value = (False, "")
    #             from app.lamconnect.lamconnect import app

    #             app.testing = True
    #             with app.test_client() as client:
    #                 body = {
    #                     "user_identification": "123456",
    #                     "customer_id": "789012",
    #                     "operational_unit_id": "345678",
    #                 }
    #                 mimetype = "application/json"
    #                 headers = {
    #                     "Content-Type": mimetype,
    #                     "Accept": mimetype,
    #                     "Authorization": "123456",
    #                 }
    #                 response_code = client.post(
    #                     "/orderbook_by_customer_id_and_operational_unit_id",
    #                     data=json.dumps(body),
    #                     headers=headers,
    #                 )._status_code
    #                 self.assertEqual(response_code, 500)

    #     with mock.patch("app.lamconnect.lamconnect.get_generic_query") as get_generic_query_mock:
    #         with mock.patch("app.lamconnect.lamconnect.AWS.get_from_secret_manager") as get_secret_mock:
    #             get_secret_mock.return_value = "123456"
    #             get_generic_query_mock.return_value = (True, "")
    #             from app.lamconnect.lamconnect import app

    #             app.testing = True
    #             with app.test_client() as client:
    #                 body = {
    #                     "user_identification": "123456",
    #                     "customer_id": "789012",
    #                     "operational_unit_id": "345678",
    #                 }
    #                 mimetype = "application/json"
    #                 headers = {
    #                     "Content-Type": mimetype,
    #                     "Accept": mimetype,
    #                     "Authorization": "123456",
    #                 }

    #                 response_code = client.post(
    #                     "/orderbook_by_customer_id_and_operational_unit_id",
    #                     data=json.dumps(body),
    #                     headers=headers,
    #                 )._status_code
    #                 self.assertEqual(response_code, 200)

    #                 response = client.post(
    #                     "/orderbook_by_customer_id_and_operational_unit_id",
    #                     data=json.dumps(body),
    #                     headers=None,
    #                 )
    #                 self.assertEqual(response.json, {"message": "A token is mandatory"})

    #                 headers = {
    #                     "Content-Type": mimetype,
    #                     "Accept": mimetype,
    #                     "Authorization": "Bearer *12346",
    #                 }

    #                 response = client.post(
    #                     "/orderbook_by_customer_id_and_operational_unit_id",
    #                     data=json.dumps(body),
    #                     headers=headers,
    #                 )
    #                 self.assertEqual(response.json, {"message": "token is invalid"})
