import connexion
import uuid
from drm_appointment.models.patient import Patient as PatientData  # noqa: E501
from drm_appointment.models.models_sqlalchemy import Patient

from drm_appointment.database import db


def add_patient(patient=None):  # noqa: E501
    """Add a new patient

     # noqa: E501

    :param patient:
    :type patient: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        patient = PatientData.from_dict(connexion.request.get_json())  # noqa: E501

        patient_model = Patient()
        patient_model.id = str(uuid.uuid1())
        patient_model.name = patient.name

        db.session.add(patient_model)
        db.session.commit()

        patient.id = patient_model.id

    return patient, 201


def search_patients(search_name=None):  # noqa: E501
    """list patients

    By passing in the appropriate options, you can search for available patients in the system  # noqa: E501

    :param search_name: pass an optional search string for looking up patient name
    :type search_name: str

    :rtype: List[Patient]
    """
    if search_name:
        patients = (
            db.session.query(Patient.id, Patient.name)
            .filter(Patient.name.contains(f"%{search_name}%"))
            .order_by(Patient.name)
            .all()
        )
    else:
        patients = db.session.query(Patient.id, Patient.name).order_by(Patient.name).all()

    return [
        {
            "id": patient[0],
            "name": patient[1],
        }
        for patient in patients
    ], 200


def update_patient(patient=None):  # noqa: E501
    """Updates a patient

     # noqa: E501

    :param patient:
    :type patient: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        patient = PatientData.from_dict(connexion.request.get_json())  # noqa: E501

        patient_model = Patient().query.get(patient.id)
        if patient_model:
            patient_model.name = patient.name
            db.session.commit()
            return None, 200
        else:
            return None, 404
