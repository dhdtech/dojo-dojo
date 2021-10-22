import connexion
import six

from drm_financial.models.charge_data import ChargeData  # noqa: E501
from drm_financial.models.models_sqlalchemy import Charge
from drm_financial import util
from drm_appointment.worker import celery
import celery.states as states
from sqlalchemy.exc import IntegrityError

from drm_appointment.database import db


def add_charge(charge_data=None):  # noqa: E501
    """Calculate amount for appointment

     # noqa: E501

    :param charge_data:
    :type charge_data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        charge_data = ChargeData.from_dict(connexion.request.get_json())  # noqa: E501

        charge_model = Charge()
        charge_model.appointment_id = charge_data.appointment_id
        charge_model.amount = charge_data.total_price
        db.session.add(charge_model)

        try:
            db.session.commit()
        except IntegrityError:
            return "Valid apponintment is mandatory.", 400

        charge_data.id = charge_model.id

    return charge_data, 201
