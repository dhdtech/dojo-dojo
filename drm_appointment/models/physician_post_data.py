# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from drm_appointment.models.base_model_ import Model
from drm_appointment import util


class PhysicianPostData(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None):  # noqa: E501
        """PhysicianPostData - a model defined in OpenAPI

        :param name: The name of this PhysicianPostData.  # noqa: E501
        :type name: str
        """
        self.openapi_types = {"name": str}

        self.attribute_map = {"name": "name"}

        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> "PhysicianPostData":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PhysicianPostData of this PhysicianPostData.  # noqa: E501
        :rtype: PhysicianPostData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this PhysicianPostData.


        :return: The name of this PhysicianPostData.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PhysicianPostData.


        :param name: The name of this PhysicianPostData.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name
