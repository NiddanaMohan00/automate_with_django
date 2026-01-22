from django.core.management.base import BaseCommand,CommandError
from django.db import DataError
from dataentry.models import Student
import csv
from django.apps import apps
#proposed command - python manage.py importdata file_path model_name

class Command(BaseCommand):
    help="import data from CSV file into the database"
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file to be imported')
        parser.add_argument('model_name', type=str, help='Name of the model to import data into')
    def handle(self,*args,**kwargs):
        
        #logic to import data from CSV file into the database
        file_path=kwargs['file_path']
        model_name=kwargs['model_name'].capitalize()
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
        
        #compare csv headers with model fields
        #get model fields
        # model_fields=[field.name for field in model._meta.fields][1:] #excluding id field
        model_fields=[field.name for field in model._meta.fields if field.name != 'id'] #excluding id field

        with open(file_path,'r') as file:
            reader=csv.DictReader(file)
            csv_fields=reader.fieldnames
            
            # print(reader)
            # for row in reader:
            #     print(row)
            if csv_fields != model_fields:
                raise DataError(f'CSV headers {csv_fields} do not match model fields {model_fields}')
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully'))
    