#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django.conf import settings
from tddspry.django import HttpTestCase
from djtest.hello.views import CalendarWidget

class TestCalendar(HttpTestCase):

    def test_content(self):
        self.go200('/edit_contacts_form/')
        self.url('/accounts/login/\?next=/edit_contacts_form/')
        self.submit200()
        self.go200('/edit_contacts_form/')
        self.url('/edit_contacts_form/')
        self.find('vDateField')
        #Перевірка загрузки медіа-лінків

        for jslink in CalendarWidget.Media.js:
            self.go200(jslink)

        for csslinks_for_media in CalendarWidget.Media.css.values():
            for csslink in csslinks_for_media:
                self.go200(csslink)

    def test_form_order(self):
        self.extend_with('match_parse')
        self.go('/accounts/logout/')
        self.go('/edit_contacts_form/')
        self.url('/accounts/login/\?next=/edit_contacts_form/')
        self.fv(1, 'username', 'admin')
        self.fv(1, 'password', 'admin')
        self.submit()
        self.go('/edit_contacts_form/')
        #mlist = self.findall('name=.(birth_date|first_name).')
        self.ok_(False)
