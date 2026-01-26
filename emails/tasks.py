from awd_main.celery import app
from dataentry.utils import send_email_nottification
@app.task
def send_email_task(mail_subject,message,to_email,attachments):
    send_email_nottification(mail_subject,message,to_email,attachments)
    return "Email sending task completed!"