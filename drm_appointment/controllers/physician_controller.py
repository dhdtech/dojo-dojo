import connexion
import uuid
from drm_appointment.models.physician import Physician as PhysicianData  # noqa: E501
from drm_appointment.models.models_sqlalchemy import Physician


from drm_appointment.database import db


def add_physician(physician=None):  # noqa: E501
    """Add a new physician

     # noqa: E501

    :param physician:
    :type physician: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        physician = PhysicianData.from_dict(connexion.request.get_json())  # noqa: E501

        physician_model = Physician()
        physician_model.id = str(uuid.uuid1())
        physician_model.name = physician.name

        db.session.add(physician_model)
        db.session.commit()

        physician.id = physician_model.id

    return physician, 201


def search_physicians(search_name=None):  # noqa: E501
    """list physicians

    By passing in the appropriate options, you can search for available physicians in the system  # noqa: E501

    :param search_name: pass an optional search string for looking up physician name
    :type search_name: str

    :rtype: List[Physician]
    """
    if search_name:
        physicians = (
            db.session.query(Physician.id, Physician.name)
            .filter(Physician.name.contains(f"%{search_name}%"))
            .order_by(Physician.name)
            .all()
        )
    else:
        physicians = db.session.query(Physician.id, Physician.name).order_by(Physician.name).all()

    return [
        {
            "id": physician[0],
            "name": physician[1],
        }
        for physician in physicians
    ], 200


def update_physician(physician=None):  # noqa: E501
    """Updates a physician

     # noqa: E501

    :param physician:
    :type physician: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        physician = PhysicianData.from_dict(connexion.request.get_json())  # noqa: E501

        physician_model = Physician().query.get(physician.id)
        if physician_model:
            physician_model.name = physician.name
            db.session.commit()
            return None, 200
        else:
            return None, 404
