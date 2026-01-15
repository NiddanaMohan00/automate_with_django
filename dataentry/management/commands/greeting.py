from django.core.management.base import BaseCommand

#proposed command =python manage.py greeting john
#expected output = Greetings from Django! john
class Command(BaseCommand):
    help='Prints a greeting to the console'
    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name to greet')
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Greetings from Django! {options["name"]}'))