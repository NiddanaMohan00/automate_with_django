from django.core.management.base import BaseCommand,CommandError
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
        
            
        with open(file_path,'r') as file:
            reader=csv.DictReader(file)
            # print(reader)
            # for row in reader:
            #     print(row)
            for row in reader:
        
                model.objects.create(**row)
                    
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully'))
    