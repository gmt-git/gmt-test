#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget

from djtest.hello.models import Contacts

class CalendarWidget(forms.TextInput):
    class Media:
        js = (
            '/static_media/js/jquery.js',
            '/static_media/datePicker/date.js',
            '/static_media/datePicker/jquery.datePicker.js'
        )

        css = {'all': ('/static_media/datePicker/datePicker.css', )}

    def __init__(self):
        super(CalendarWidget, self).__init__(attrs={'class': 'date-pick'})

class ContactsFormT5(forms.ModelForm):
    class Meta:
        model = Contacts

class ContactsForm(forms.ModelForm):
    birth_date = forms.DateField(widget=CalendarWidget())
    class Media:
        js = ('/static_media/js/jquery.js',
            '/static_media/js/jquery.form.js',
            '/static_media/hello/js/contacts_form.js')

        css = { 'all': (
            '/static_media/hello/css/datePicker.css',
            '/media/css/base.css',
        )}

    class Meta:
        model = Contacts
        fields = ('birth_date', 'contact_email', 'last_name', 'first_name')
