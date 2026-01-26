from django.shortcuts import render,redirect
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_nottification
from django.conf import settings
from .models import Subscriber
from .tasks import send_email_task
# Create your views here.
def send_email(request):
    if request.method=="POST":
        email_form=EmailForm(request.POST,request.FILES)
        if email_form.is_valid():
            email_form=email_form.save()
            #send an email
            mail_subject=request.POST.get('subject')
            message=request.POST.get('body')
            email_list=request.POST.get('email_list')
            # print(email_list)#1
            
            #access the selected email list
            email_list=email_form.email_list
            #extract email addresses from the subscriber model in the selected email list
            subscribers=Subscriber.objects.filter(email_list=email_list)
            to_email=[email.email_address for email in subscribers]
        
            if email_form.attachment:
                attachments=email_form.attachment.path
                
            else:
                attachments=None
            #headover email sending to the celery
            send_email_task.delay(mail_subject,message,to_email,attachments)
            #send_email_nottification(mail_subject,message,to_email,attachments)
            #display a success message
            messages.success(request,"Email sent successfully!")
            return redirect('send_email')
    else:
        email_form=EmailForm()
        context={
            'email_form':email_form
        }
        return render(request,'emails/send-email.html',context)
