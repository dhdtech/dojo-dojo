# coding: utf-8

from __future__ import absolute_import
import unittest
from unittest import mock

from flask import json
from six import BytesIO
from drm_appointment.worker import celery

from drm_appointment.models.appointment import Appointment  # noqa: E501
from drm_appointment.test import BaseTestCase


class TestAppointmentController(BaseTestCase):
    """AppointmentController integration test stubs"""

    def setUp(self):
        self.headers = {"Authorization": "Bearer 123456789"}

        patient = {"name": "Patient full name 2"}
        response = self.client.open(
            "/1.0.0/patient",
            method="POST",
            headers=self.headers,
            data=json.dumps(patient),
            content_type="application/json",
        )
        self.existant_patient_id = response.json.get("id")

        physician = {"name": "Physician full name 2"}
        response = self.client.open(
            "/1.0.0/physician",
            method="POST",
            headers=self.headers,
            data=json.dumps(physician),
            content_type="application/json",
        )
        self.existant_physician_id = response.json.get("id")

        appointment = {
            "end_date": "2021-01-30T09:30:00Z",
            "patient": {"id": self.existant_patient_id},
            "price": 200.0,
            "physician": {"id": self.existant_physician_id},
            "start_date": "2021-01-30T08:30:00Z",
        }

        response = self.client.open(
            "/1.0.0/appointment",
            method="POST",
            headers=self.headers,
            data=json.dumps(appointment),
            content_type="application/json",
        )
        self.existant_appointment_id = response.json.get("id")

    def test_appointment_post_sucess(self):
        """Test case for appointment_post

        Add a new appointment
        """
        appointment = {
            "end_date": "2021-01-30T09:30:00Z",
            "patient": {"id": self.existant_patient_id},
            "price": 200.0,
            "physician": {"id": self.existant_physician_id},
            "start_date": "2021-01-30T08:30:00Z",
        }
        response = self.client.open(
            "/1.0.0/appointment",
            method="POST",
            headers=self.headers,
            data=json.dumps(appointment),
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_start_appointment(self):
        """Test case for start_appointment

        Add a new appointment
        """
        appointment = {"patient_id": self.existant_patient_id, "physician_id": self.existant_physician_id}
        response = self.client.open(
            "/1.0.0/appointment/startAppointment",
            method="POST",
            headers=self.headers,
            data=json.dumps(appointment),
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_start_appointment_wrong_patient(self):
        """Test case for start_appointment

        Add a new appointment
        """
        appointment = {
            "patient_id": "d290f1ee-6c54-4b01-90e6-d701748f000",
            "physician_id": self.existant_physician_id,
        }
        response = self.client.open(
            "/1.0.0/appointment/startAppointment",
            method="POST",
            headers=self.headers,
            data=json.dumps(appointment),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_end_appointment(self):
        """Test case for start_appointment

        Add a new appointment
        """
        celery.send_task = mock.MagicMock()
        appointment = {"appointment_id": self.existant_appointment_id}
        response = self.client.open(
            "/1.0.0/appointment/endAppointment",
            method="POST",
            headers=self.headers,
            data=json.dumps(appointment),
            content_type="application/json",
        )
        self.assert200(response)

    def test_end_appointment_wrong_id(self):
        """Test case for start_appointment

        Add a new appointment
        """
        appointment = {"appointment_id": "d290f1ee-6c54-4b01-90e6-d701748f000"}
        response = self.client.open(
            "/1.0.0/appointment/endAppointment",
            method="POST",
            headers=self.headers,
            data=json.dumps(appointment),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_appointment_post_wrong_physician(self):
        """Test case for appointment_post

        Add a new appointment
        """
        appointment = {
            "end_date": "2021-01-30T09:30:00Z",
            "patient": {"id": self.existant_patient_id},
            "price": 200.0,
            "physician": {"id": "d290f1ee-6c54-4b01-90e6-d701748f085"},
            "start_date": "2021-01-30T08:30:00Z",
        }
        response = self.client.open(
            "/1.0.0/appointment",
            method="POST",
            headers=self.headers,
            data=json.dumps(appointment),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_not_found_appointment_put(self):
        """Test case for appointment_put

        Updates a physician
        """
        appointment = {
            "end_date": "2021-01-30T09:30:00Z",
            "patient": {"name": "Patient full name", "id": "d290f1ee-6c54-4b01-90e6-d701748f0851"},
            "price": 200.0,
            "physician": {"name": "Physician full name", "id": "d290f1ee-6c54-4b01-90e6-d701748f0851"},
            "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
            "start_date": "2021-01-30T08:30:00Z",
        }
        response = self.client.open(
            "/1.0.0/appointment",
            method="PUT",
            headers=self.headers,
            data=json.dumps(appointment),
            content_type="application/json",
        )
        self.assert404(response, "Response body is : " + response.data.decode("utf-8"))

    def test_found_appointment_put(self):
        """Test case for appointment_put

        Updates a physician
        """

        appointment = {
            "end_date": "2021-01-30T09:30:00Z",
            "patient": {"id": self.existant_patient_id},
            "price": 200.0,
            "physician": {"id": self.existant_physician_id},
            "id": self.existant_appointment_id,
            "start_date": "2021-01-30T08:30:00Z",
        }

        response = self.client.open(
            "/1.0.0/appointment",
            method="PUT",
            headers=self.headers,
            data=json.dumps(appointment),
            content_type="application/json",
        )

        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_search_appointments(self):
        """Test case for search_appointments

        list appointments
        """
        query_string = [("searchPatient", self.existant_patient_id), ("searchPhysician", self.existant_physician_id)]
        response = self.client.open("/1.0.0/appointment", method="GET", headers=self.headers, query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
