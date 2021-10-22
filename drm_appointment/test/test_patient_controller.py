# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from drm_appointment.models.patient import Patient  # noqa: E501
from drm_appointment.test import BaseTestCase


class TestPatientController(BaseTestCase):
    """PatientController integration test stubs"""

    def test_patient_post(self):
        """Test case for patient_post

        Add a new patient
        """
        patient = {"name": "Patient full name"}
        headers = {"Authorization": "Bearer 123456789"}
        response = self.client.open(
            "/1.0.0/patient",
            method="POST",
            headers=headers,
            data=json.dumps(patient),
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_not_found_patient_put(self):
        """Test case for patient_put

        Updates a patient
        """
        patient = {"name": "Patient full name 2"}
        headers = {"Authorization": "Bearer 123456789"}
        response = self.client.open(
            "/1.0.0/patient",
            method="PUT",
            headers=headers,
            data=json.dumps(patient),
            content_type="application/json",
        )
        # Test for not found patient
        self.assert404(response, "Response body is : " + response.data.decode("utf-8"))

    def test_found_patient_put(self):
        """Test case for patient_put

        Updates a patient
        """
        new_patient = {"name": "Patient full name 2"}
        headers = {"Authorization": "Bearer 123456789"}

        response = self.client.open(
            "/1.0.0/patient",
            method="POST",
            headers=headers,
            data=json.dumps(new_patient),
            content_type="application/json",
        )

        updatable_patient = {"name": "Updated Name", "id": response.json.get("id")}
        response = self.client.open(
            "/1.0.0/patient",
            method="PUT",
            headers=headers,
            data=json.dumps(updatable_patient),
            content_type="application/json",
        )
        # Test for not found patient
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_search_patients(self):
        """Test case for search_patients

        list patients
        """
        query_string = [("searchName", "Patient")]
        headers = {"Authorization": "Bearer 123456789"}
        response = self.client.open("/1.0.0/patient", method="GET", headers=headers, query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

        query_string = None
        response = self.client.open("/1.0.0/patient", method="GET", headers=headers, query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
