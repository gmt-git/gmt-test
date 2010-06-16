from django.shortcuts import render_to_response
from djtest.hello.models import Contacts

def home_page(request):
    obj = Contacts.objects.get(contact_email='gmt.more@gmail.com')
    
    return render_to_response('home_page.html',
        {
            "first_name" : obj.first_name,
            "last_name" : obj.last_name,
            "contact_email" : obj.contact_email,
        })
