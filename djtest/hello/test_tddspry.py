#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django.conf import settings
from tddspry.django import HttpTestCase

class TestCalendar(HttpTestCase):

    def test_content(self):
        self.go200('/edit_contacts_form/')
        self.url('/accounts/login/\?next=/edit_contacts_form/')
        self.submit200()
        self.go200('/edit_contacts_form/')
        self.url('/edit_contacts_form/')
        self.find('DateField')
