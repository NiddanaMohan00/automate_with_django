from django.contrib import admin
from .models import Employee, Student, Customer
# Register your models here.
admin.site.register(Student)
admin.site.register(Customer)
admin.site.register(Employee)