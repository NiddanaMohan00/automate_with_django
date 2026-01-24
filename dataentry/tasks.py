from awd_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from dataentry.utils import send_email_nottification
@app.task
def celery_test_task():
    
    time.sleep(5)  # Simulating a time-consuming task
    #send an email notification 
    mail_subject='Test Subject'
    message='This is a test email from Celery task.'
    to_email=settings.DEFAULT_TO_EMAIL
    send_email_nottification(mail_subject,message,to_email)
    return "Email sent successfully!"
@app.task
def import_data_task(file_path,model_name):
    try:
        call_command('importdata',file_path,model_name)
    except Exception as e:
        raise e
    #notify the user by email
    mail_subject='Data Import Successful'
    message=f'Data has been successfully imported into the {model_name} model.'
    to_email=settings.DEFAULT_TO_EMAIL
    
    send_email_nottification(mail_subject,message,to_email)
 
    return "Data imported successfully!"
