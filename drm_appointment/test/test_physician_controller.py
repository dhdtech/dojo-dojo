# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from drm_appointment.models.physician import Physician  # noqa: E501
from drm_appointment.test import BaseTestCase


class TestPhysicianController(BaseTestCase):
    """PhysicianController integration test stubs"""

    def test_physician_post(self):
        """Test case for physician_post

        Add a new physician
        """
        physician = {"name": "Physician full name"}
        headers = {"Authorization": "Bearer 123456789"}
        response = self.client.open(
            "/1.0.0/physician",
            method="POST",
            headers=headers,
            data=json.dumps(physician),
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_not_found_physician_put(self):
        """Test case for physician_put

        Updates a physician
        """
        physician = {"name": "Physician full name 2"}
        headers = {"Authorization": "Bearer 123456789"}
        response = self.client.open(
            "/1.0.0/physician",
            method="PUT",
            headers=headers,
            data=json.dumps(physician),
            content_type="application/json",
        )
        # Test for not found physician
        self.assert404(response, "Response body is : " + response.data.decode("utf-8"))

    def test_found_physician_put(self):
        """Test case for physician_put

        Updates a physician
        """
        new_physician = {"name": "Physician full name 2"}
        headers = {"Authorization": "Bearer 123456789"}

        response = self.client.open(
            "/1.0.0/physician",
            method="POST",
            headers=headers,
            data=json.dumps(new_physician),
            content_type="application/json",
        )

        updatable_physician = {"name": "Updated Name", "id": response.json.get("id")}
        response = self.client.open(
            "/1.0.0/physician",
            method="PUT",
            headers=headers,
            data=json.dumps(updatable_physician),
            content_type="application/json",
        )
        # Test for not found physician
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_search_physicians(self):
        """Test case for search_physicians

        list physicians
        """
        query_string = [("searchName", "Physician")]
        headers = {"Authorization": "Bearer 123456789"}
        response = self.client.open("/1.0.0/physician", method="GET", headers=headers, query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

        query_string = None
        response = self.client.open("/1.0.0/physician", method="GET", headers=headers, query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
