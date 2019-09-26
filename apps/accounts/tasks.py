from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from config.celery import app
from config.settings import DEFAULT_FROM_EMAIL
logger=get_task_logger(__name__)


@app.task(bind=True)
def AsyncEmail(self, email, title, message):
    logger.info('Sent email')
    return send_mail(subject=title, message=message, recipient_list=[email], from_email=DEFAULT_FROM_EMAIL,
              fail_silently=False, html_message=message)
