from datetime import datetime
import connexion
import uuid
from drm_appointment.worker import celery

from drm_appointment.models.appointment import Appointment as AppointmentData  # noqa: E501
from drm_appointment.models.start_appointment_data import StartAppointmentData  # noqa: E501
from drm_appointment.models.end_appointment_data import EndAppointmentData  # noqa: E501
from drm_appointment.models.models_sqlalchemy import Appointment, Physician, Patient
from drm_appointment.database import db


def add_appointment():  # noqa: E501
    """Add a new appointment
     # noqa: E501
    :rtype: None
    """
    if connexion.request.is_json:
        appointment = AppointmentData.from_dict(connexion.request.get_json())  # noqa: E501

        physician = _get_physician(appointment.physician.id)
        patient = _get_patient(appointment.patient.id)

        if not physician or not patient:
            return "Valid physician and patiens are mandatory.", 400

        appointment_model = Appointment()
        appointment_model.id = str(uuid.uuid1())
        appointment_model.start_date = appointment.start_date
        appointment_model.end_date = appointment.end_date
        appointment_model.physician = physician
        appointment_model.patient = patient
        appointment_model.price = appointment.price

        db.session.add(appointment_model)
        db.session.commit()

        appointment.id = appointment_model.id

    return appointment, 201


def start_appointment():  # noqa: E501
    """Starts a new appointment
     # noqa: E501
    :rtype: None
    """
    if connexion.request.is_json:
        appointment = StartAppointmentData.from_dict(connexion.request.get_json())  # noqa: E501

        physician = _get_physician(appointment.physician_id)
        patient = _get_patient(appointment.patient_id)

        if not physician or not patient:
            return "Valid physician and patiens are mandatory.", 400

        appointment_model = Appointment()
        appointment_model.id = str(uuid.uuid1())
        appointment_model.start_date = datetime.now()
        appointment_model.physician = physician
        appointment_model.patient = patient

        db.session.add(appointment_model)
        db.session.commit()

        appointment.id = appointment_model.id

    return appointment, 201


def end_appointment():  # noqa: E501
    """Ends an appointment

     # noqa: E501

    :rtype: None
    """
    if connexion.request.is_json:
        appointment = EndAppointmentData.from_dict(connexion.request.get_json())  # noqa: E501

        appointment_model = Appointment().query.get(appointment.appointment_id)
        if appointment_model:
            return calculate_save_and_call_task_for_appointment(appointment_model)
        else:
            return "Appointment not found", 404


def calculate_save_and_call_task_for_appointment(appointment_model):
    """Calculate total of hours, save data anda and call async task.

     # noqa: E501

    :rtype: None
    """
    start_date = appointment_model.start_date
    end_date = datetime.now()
    total_time_in_hours = (end_date - start_date).total_seconds() / 3600
    price = total_time_in_hours * 200
    appointment_model.end_date = end_date
    appointment_model.price = price

    db.session.commit()
    celery.send_task("tasks.add_charge", args=[appointment_model.id, appointment_model.price], kwargs={})

    return None, 200


def search_appointments(search_patient=None, search_physician=None):  # noqa: E501
    """list appointments

    By passing in the appropriate options, you can search for available appointments in the system  # noqa: E501

    :param search_patient: pass an optional search string for looking up patients name
    :type search_patient: str
    :param search_physician: pass an optional search string for looking up physicians name
    :type search_physician: str

    :rtype: List[Appointment]
    """
    query_filter = {}
    if search_patient:
        query_filter["patient_id"] = search_patient

    if search_physician:
        query_filter["physician_id"] = search_physician

    appointments = db.session.query(Appointment).filter_by(**query_filter).order_by(Appointment.start_date).all()

    return [
        {
            "id": appointment.id,
            "start_date": appointment.start_date,
            "end_date": appointment.end_date,
            "physician": appointment.physician.id,
            "patient": appointment.patient.id,
            "price": appointment.price,
        }
        for appointment in appointments
    ], 200


def update_appointment():  # noqa: E501
    """Updates a appointment

    # noqa: E501
    """
    if connexion.request.is_json:
        appointment = AppointmentData.from_dict(connexion.request.get_json())  # noqa: E501

        appointment_model = Appointment().query.get(appointment.id)
        if not appointment_model:
            return None, 404

        if appointment.start_date:
            appointment_model.start_date = appointment.start_date
        if appointment.end_date:
            appointment_model.end_date = appointment.end_date
        if appointment.physician:
            appointment_model.physician_id = appointment.physician.id
        if appointment.patient:
            appointment_model.patient_id = appointment.patient.id
        if appointment.price:
            appointment_model.price = appointment.price

        db.session.commit()
        return None, 200


def _get_patient(patient_id):
    return Patient.query.get(patient_id)


def _get_physician(physician_id):
    return Physician.query.get(physician_id)
