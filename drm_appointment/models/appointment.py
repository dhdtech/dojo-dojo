# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from drm_appointment.models.base_model_ import Model
from drm_appointment.models.patient import Patient
from drm_appointment.models.physician import Physician
from drm_appointment import util

from drm_appointment.models.patient import Patient  # noqa: E501
from drm_appointment.models.physician import Physician  # noqa: E501


class Appointment(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, start_date=None, end_date=None, physician=None, patient=None, price=None):  # noqa: E501
        """Appointment - a model defined in OpenAPI

        :param id: The id of this Appointment.  # noqa: E501
        :type id: str
        :param start_date: The start_date of this Appointment.  # noqa: E501
        :type start_date: datetime
        :param end_date: The end_date of this Appointment.  # noqa: E501
        :type end_date: datetime
        :param physician: The physician of this Appointment.  # noqa: E501
        :type physician: Physician
        :param patient: The patient of this Appointment.  # noqa: E501
        :type patient: Patient
        :param price: The price of this Appointment.  # noqa: E501
        :type price: float
        """
        self.openapi_types = {
            "id": str,
            "start_date": datetime,
            "end_date": datetime,
            "physician": Physician,
            "patient": Patient,
            "price": float,
        }

        self.attribute_map = {
            "id": "id",
            "start_date": "start_date",
            "end_date": "end_date",
            "physician": "physician",
            "patient": "patient",
            "price": "price",
        }

        self._id = id
        self._start_date = start_date
        self._end_date = end_date
        self._physician = physician
        self._patient = patient
        self._price = price

    @classmethod
    def from_dict(cls, dikt) -> "Appointment":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Appointment of this Appointment.  # noqa: E501
        :rtype: Appointment
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Appointment.


        :return: The id of this Appointment.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Appointment.


        :param id: The id of this Appointment.
        :type id: str
        """

        self._id = id

    @property
    def start_date(self):
        """Gets the start_date of this Appointment.


        :return: The start_date of this Appointment.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this Appointment.


        :param start_date: The start_date of this Appointment.
        :type start_date: datetime
        """

        self._start_date = start_date

    @property
    def end_date(self):
        """Gets the end_date of this Appointment.


        :return: The end_date of this Appointment.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this Appointment.


        :param end_date: The end_date of this Appointment.
        :type end_date: datetime
        """

        self._end_date = end_date

    @property
    def physician(self):
        """Gets the physician of this Appointment.


        :return: The physician of this Appointment.
        :rtype: Physician
        """
        return self._physician

    @physician.setter
    def physician(self, physician):
        """Sets the physician of this Appointment.


        :param physician: The physician of this Appointment.
        :type physician: Physician
        """

        self._physician = physician

    @property
    def patient(self):
        """Gets the patient of this Appointment.


        :return: The patient of this Appointment.
        :rtype: Patient
        """
        return self._patient

    @patient.setter
    def patient(self, patient):
        """Sets the patient of this Appointment.


        :param patient: The patient of this Appointment.
        :type patient: Patient
        """

        self._patient = patient

    @property
    def price(self):
        """Gets the price of this Appointment.


        :return: The price of this Appointment.
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this Appointment.


        :param price: The price of this Appointment.
        :type price: float
        """

        self._price = price