import csv

from django.core.management.base import BaseCommand,CommandError
# from dataentry.models import Student
import datetime
#proposed command - python manage.py exportdata modele_name
from django.apps import apps
from dataentry.utils import generate_csv_file
class Command(BaseCommand):
    help="export data from student database to a csv file"
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model to export data from')
        
    
    def handle(self, *args, **kwargs):
        model_name=kwargs['model_name'].capitalize()
        #search for model across all installed apps
        model=None
        for app_config in apps.get_app_configs():
            #try to get the model
            try:
                model=apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue
        if not model:
            self.stdout.write(self.style.ERROR(f'Model "{model_name}" not found in any installed app.'))
            return
           
        
        #fetch data from the database
        else:
            data=model.objects.all()
            #generate the csv file
            file_path=generate_csv_file(model_name)
            
            # print(file_path)
            
            with open(file_path,'w',newline='') as file:
                writer=csv.writer(file)
                #write the csv header
                #we want to print the field names of the model
                writer.writerow([field.name for field in model._meta.fields])
                
                #write the data rows
                for dt in data:
                    writer.writerow([getattr(dt,field.name)for field in model._meta.fields])
                    
            self.stdout.write(self.style.SUCCESS(f"Data exported to {file_path}"))