# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from drm_financial.models.base_model_ import Model
from drm_financial import util


class ChargeData(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, appointment_id=None, total_price=None):  # noqa: E501
        """ChargeData - a model defined in OpenAPI

        :param appointment_id: The appointment_id of this ChargeData.  # noqa: E501
        :type appointment_id: str
        :param total_price: The total_price of this ChargeData.  # noqa: E501
        :type total_price: float
        """
        self.openapi_types = {"appointment_id": str, "total_price": float}

        self.attribute_map = {"appointment_id": "appointment_id", "total_price": "total_price"}

        self._appointment_id = appointment_id
        self._total_price = total_price

    @classmethod
    def from_dict(cls, dikt) -> "ChargeData":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ChargeData of this ChargeData.  # noqa: E501
        :rtype: ChargeData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def appointment_id(self):
        """Gets the appointment_id of this ChargeData.


        :return: The appointment_id of this ChargeData.
        :rtype: str
        """
        return self._appointment_id

    @appointment_id.setter
    def appointment_id(self, appointment_id):
        """Sets the appointment_id of this ChargeData.


        :param appointment_id: The appointment_id of this ChargeData.
        :type appointment_id: str
        """
        if appointment_id is None:
            raise ValueError("Invalid value for `appointment_id`, must not be `None`")  # noqa: E501

        self._appointment_id = appointment_id

    @property
    def total_price(self):
        """Gets the total_price of this ChargeData.


        :return: The total_price of this ChargeData.
        :rtype: float
        """
        return self._total_price

    @total_price.setter
    def total_price(self, total_price):
        """Sets the total_price of this ChargeData.


        :param total_price: The total_price of this ChargeData.
        :type total_price: float
        """
        if total_price is None:
            raise ValueError("Invalid value for `total_price`, must not be `None`")  # noqa: E501

        self._total_price = total_price