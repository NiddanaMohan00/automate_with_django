from django.shortcuts import redirect, render
from .utils import get_all_custom_models
from django.conf import settings
from uploads.models import Upload
from django.core.management import call_command

from django.contrib import messages
from dataentry.utils import check_csv_errors
from .tasks import import_data_task,export_data_task
from django.core.management import call_command
# Create your views here.
def import_data(request):
    if request.method=='POST':
        file_path=request.FILES.get('file_path')
        model_name=request.POST.get('model_name')
        #store this file inside the Upload model
        upload=Upload.objects.create(file=file_path,model_name=model_name)
        #construct the full path
        relative_path=upload.file.name  #uploads/filename.csv
        base_url=settings.BASE_DIR       #trigger the import data command
        file_path=str(base_url/'media'/relative_path)
        #check for the  csv errors
        try:
            check_csv_errors(file_path,model_name)
        except Exception as e:
            messages.error(request,f'Error in CSV file: {str(e)}')
            return redirect('import_data')
        #handle the importdata task
        import_data_task.delay(file_path,model_name)
        
        #show the message to the user
        messages.success(request,'Data import has been initiated. You will be notified once it is complete.')
        
        return redirect('import_data')
    else:
        custom_models=get_all_custom_models()
        context={'custom_models':custom_models}
    return render(request,'dataentry/importdata.html',context)


def export_data(request):
    if request.method=='POST':
        model_name=request.POST.get('model_name')
        #call the export data task
        export_data_task.delay(model_name)
        messages.success(request,'Data export has been initiated. You will be notified once it is complete.')
        return redirect('export_data')

    else:
        custom_models=get_all_custom_models()
        context={'custom_models':custom_models}
    return render(request,'dataentry/exportdata.html',context)
    
