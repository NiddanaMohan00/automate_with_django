from django.apps import apps
from django.core.management.base import BaseCommand,CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os
def get_all_custom_models():
    #try to get all the apps
    default_models=['Group','Permission','LogEntry','ContentType','Session','User']
    custom_models=[]
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models

def check_csv_errors(file_path,model_name):
    #this function will check for csv errors
    #for now we will just return an empty list
    model=None
    #Search for model across all installed apps
    for app_config in apps.get_app_configs():
        #Try to get the model
        try:
            model=apps.get_model(app_config.label, model_name)
            
            break
        except LookupError:
            continue
    if not model:
        raise CommandError(f'Model "{model_name}" not found in any installed app.')
    
    model_fields=[field.name for field in model._meta.fields if field.name != 'id'] #excluding id field
    try:
        with open(file_path,'r') as file:
            reader=csv.DictReader(file)
            csv_fields=reader.fieldnames
            
            
            if csv_fields != model_fields:
                raise DataError(f'CSV headers {csv_fields} do not match model fields {model_fields}')
    except Exception as e:
        raise e
    return model


def send_email_nottification(mail_subject,message,to_email,attachments=None):
    
    try:
        from_email=settings.DEFAULT_FROM_EMAIL
        mail=EmailMessage(mail_subject,message,from_email,to=to_email)
        if attachments is not None :
            mail.attach_file(attachments)
        mail.send()
    except Exception as e:
        raise e
    
def generate_csv_file(model_name):
    #this function will generate a csv file for the exported data
    timestamp=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    #define the csv file name/path
    export_dir='exported_data'
    file_name=f'exported_{model_name}_data_{timestamp}.csv'
    file_path=os.path.join(settings.MEDIA_ROOT,export_dir,file_name)
    print("file_path==========>",file_path)
    return file_path