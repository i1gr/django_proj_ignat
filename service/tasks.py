from celery import shared_task

from service.email_sercices import send_email_to_staff, send_email_to_customer


@shared_task
def send_mails_after_order(user_id: int):
    send_email_to_staff()
    send_email_to_customer(user_id)
