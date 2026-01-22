from django.shortcuts import redirect, render
from .utils import get_all_custom_models
from django.conf import settings
from uploads.models import Upload
from django.core.management import call_command

from django.contrib import messages
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
        print(relative_path)
        print(base_url)
        file_path=str(base_url/'media'/relative_path)
        try:
            call_command('importdata',file_path,model_name)
            messages.success(request,'Data imported successfully!')
        except Exception as e:
            messages.error(request,'Error during data import: {}'.format(e))
        return redirect('import_data')
    else:
        custom_models=get_all_custom_models()
        context={'custom_models':custom_models}
    return render(request,'dataentry/importdata.html',context)
