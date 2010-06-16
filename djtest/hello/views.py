from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from djtest.hello.models import Contacts

def home_page(request):
    obj = Contacts.objects.get(id=1)
    
    return render_to_response('home_page.html',
        {
            "first_name" : obj.first_name,
            "last_name" : obj.last_name,
            "contact_email" : obj.contact_email,
        })

def settings_cxpr(request):
    return {'settings': settings}

def cxpr_test(request):
    return render_to_response('cxpr_test.html', context_instance=RequestContext(request))
