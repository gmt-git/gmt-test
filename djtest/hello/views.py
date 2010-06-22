#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.widgets import AdminDateWidget
from djtest.hello.models import Contacts
from django.http import HttpResponseRedirect
from django import forms

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

class ContactsFormT5(forms.ModelForm):
    class Meta:
        model = Contacts

def edit_contacts(request):
    me = Contacts.objects.get(contact_email='gmt.more@gmail.com')
    if request.method == 'POST':
        form = ContactsFormT5(request.POST, instance=me)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ContactsFormT5(instance=me)

    return render_to_response('edit_contacts.html', {'form': form})

auth_req_edit_contacts = login_required(edit_contacts)

class CalendarWidget(AdminDateWidget):
    class Media:
        AMP = settings.ADMIN_MEDIA_PREFIX
        extend = False

        js = ('/admin/jsi18n/', AMP + 'js/core.js') + AdminDateWidget.Media.js

        css = {'all': (AMP + 'css/forms.css', AMP + 'css/base.css', \
            AMP + 'css/widgets.css')}

class ContactsForm(forms.ModelForm):
    birth_date = forms.DateField(widget=CalendarWidget())

    class Meta:
        model = Contacts

@login_required
def edit_contacts_form(request):
    me = Contacts.objects.get(contact_email='gmt.more@gmail.com')
    if request.method == 'POST':
        form = ContactsForm(request.POST, instance=me)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ContactsForm(instance=me)

    return render_to_response('edit_contacts_form.html', {'form': form})
