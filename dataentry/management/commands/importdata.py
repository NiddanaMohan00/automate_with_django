from django.core.management.base import BaseCommand
from django.db import DataError
from dataentry.models import Student
import csv
from django.apps import apps
from dataentry.utils import check_csv_errors
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
        model=check_csv_errors(file_path,model_name)
        with open(file_path,'r') as file:
            reader=csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully'))
    