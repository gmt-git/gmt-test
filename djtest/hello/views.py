#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from djtest.hello.models import Contacts

def home_page(request):
    obj = Contacts.objects.get(contact_email='gmt.more@gmail.com')
    
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

def edit_contacts(request):
    errors = []
    obj = Contacts.objects.all()[0]

    if request.method == 'POST':
        if not request.POST.get('first_name', ''):
            errors.append("Ім'я обов'язкове поле")
        if not request.POST.get('last_name', ''):
            errors.append("Фамілія обов'язкове поле")
        if request.POST.get('contact_email') and '@' not in request.POST['contact_email']:
            errors.append("Недійсна email адреса")
        if not errors:
            obj.first_name = request.POST['first_name']
            obj.last_name = request.POST['last_name']
            obj.contact_email = request.POST['contact_email']
            obj.save()
            return HttpResponseRedirect('/')

    return render_to_response('edit_contacts.html',
        {
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "contact_email": obj.contact_email,
            "errors": errors
        })
