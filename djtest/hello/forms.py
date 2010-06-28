#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget

from djtest.hello.models import Contacts

class CalendarWidget(AdminDateWidget):
    class Media:
        AMP = settings.ADMIN_MEDIA_PREFIX
        extend = False

        js = ('/admin/jsi18n/', AMP + 'js/core.js') + AdminDateWidget.Media.js

        css = {'all': (AMP + 'css/forms.css', AMP + 'css/base.css', \
            AMP + 'css/widgets.css')}

class ContactsFormT5(forms.ModelForm):
    class Meta:
        model = Contacts

class ContactsForm(forms.ModelForm):
    birth_date = forms.DateField(widget=CalendarWidget())

    class Meta:
        model = Contacts
        fields = ('birth_date', 'contact_email', 'last_name', 'first_name')
