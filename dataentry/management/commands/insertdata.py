#i want to add some data to the database using a custom command
from django.core.management.base import BaseCommand
from dataentry.models import Student
class Command(BaseCommand):
    help="insert data into the database"
    def handle(self, *args, **options):
        #logic to insert data into the database
        #add one student record
        dataset=[
            {"roll_no": "102", "name": "Jane Smith", "age": 22},
            {"roll_no": "103", "name": "Alice Johnson", "age": 19},
            {"roll_no": "104", "name": "Bob Brown", "age": 21}, 
            {"roll_no": "105", "name": "Charlie Davis", "age": 23}
        ]
        # Student.objects.create(roll_no="101", name="John Doe", age=20)
        # Student.objects.bulk_create([Student(**data) for data in dataset])
        for data in dataset:
            roll_no=data["roll_no"]
            existing_record=Student.objects.filter(roll_no=roll_no).exists()
            if not existing_record:
                Student.objects.create(roll_no=data["roll_no"], name=data["name"], age=data["age"])
            else:
                self.stdout.write(self.style.WARNING(f'Skipping duplicate record with roll_no: {roll_no}'))
        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))

