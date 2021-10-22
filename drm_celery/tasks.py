import os
import time
from celery import Celery
import requests


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
DRM_FINANCIAL_API_HOST = os.environ.get("DRM_FINANCIAL_API_HOST", "http://drm_financial:8080/1.0.0/")

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name="tasks.add_charge", bind=True, max_retries=10, default_retry_delay=30)
def add_charge(self, appointment_id: str, total_price: float) -> int:
    try:
        json_body = {"appointment_id": appointment_id, "total_price": total_price}
        response = requests.post(
            url=f"{DRM_FINANCIAL_API_HOST}financial/charge",
            json=json_body,
            headers={"Authorization": "Bearer 123456789"},
        )

        if response.status_code != 201:
            raise Exception

    except Exception as exc:
        raise self.retry(exc=exc)
