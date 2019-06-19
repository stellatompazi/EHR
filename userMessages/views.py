from django.shortcuts import render
from mr.models import *
from userMessages.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


# Create your views here.
def MessageForm(request):
    msg_sent = False
    if (request.method == 'POST'):
        url = request.POST.get('url')
        if (request.POST.get('receiver_id') and request.POST.get('msg_content')):
            message = Message()
            message.sender = User.objects.get(id=request.user.id)
            message.receiver = User.objects.get(id=request.POST.get('receiver_id'))
            message.content = request.POST.get('msg_content')
            message.save()

            msg_sent = True
            
            messages.add_message(request, messages.INFO, 'msg_sent')
            
            return HttpResponseRedirect(url)
   
    return HttpResponseRedirect(url)



def MessageRead(request):
	if (request.method == 'POST'):
		url = request.POST.get('url')
		if (request.POST.get('as_read')):
			message = Message.objects.get(id=request.POST.get('id'))
			message.was_read = True
			message.save()
			return HttpResponseRedirect(url)

			
	return HttpResponseRedirect(url)