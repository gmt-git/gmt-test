#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import json
import hashlib
from string import find

from django.conf import settings
from django.test import TestCase, client

from djtest.hello.models import HttpReqs, Contacts

class HelloTest(TestCase):

    def setUp(self):
        self.client = client.Client()

        initial_data_path = os.path.join(settings.PROJ_ROOT, 'hello/fixtures/initial_data.json')
        initial_data_str = open(initial_data_path).read()
        data_list = json.loads(initial_data_str)

        self.first_name = data_list[0]['fields']['first_name']
        self.last_name = data_list[0]['fields']['last_name']
        self.contact_email = data_list[0]['fields']['contact_email']

    def test_homepage_request(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)

    def test_response_context(self):
        response = self.client.get('/')

        self.failUnlessEqual(response.context['first_name'], self.first_name)
        self.failUnlessEqual(response.context['last_name'], self.last_name)
        self.failUnlessEqual(response.context['contact_email'], self.contact_email)

    def test_response_content(self):
        response = self.client.get('/')
        i1 = find(response.content, self.first_name)
        i2 = find(response.content, self.last_name)
        i3 = find(response.content, self.contact_email)
        self.failIfEqual(i1,-1)
        self.failIfEqual(i2,-1)
        self.failIfEqual(i3,-1)

class MiddlewareTest(TestCase):

    def test_middleware(self):
        hash_path = '/' + hashlib.sha1('middleware test').hexdigest() + '/?test=middleware'
        self.client = client.Client()
        self.client.get(hash_path)

        # Потім спробовати знайти по шляху запис у базі
        http_req = HttpReqs.objects.get(full_path=hash_path)

        req_tuple = (http_req.date, http_req.method, http_req.full_path, \
            http_req.meta, http_req.cookies)

class TemplateCxPrTest(TestCase):

    def test_settings_installed_apps(self):
        self.client = client.Client()
        response = self.client.get('/cxpr_test/')
        i = find(response.content, 'djtest.hello')
        self.failIfEqual(i,-1)


class EditFormTest(TestCase):

    def setUp(self):
        self.client = client.Client()

    def test_form_content(self):
        #забираємо з бази email, перевіряємо його присутність на сторінці
        contact_email = Contacts.objects.all()[0].contact_email
        response = self.client.get('/edit_contacts/')
        self.assertContains(response, contact_email)

    def test_form_post(self):
        # відправляємо нові контакти, потім перевіряємо на головній сторінці
        f_name_sha1 = hashlib.sha1('Max').hexdigest()
        l_name_sha1 = hashlib.sha1('Yuzhakov').hexdigest()
        email_sha1 = hashlib.sha1('gmt.more@gmail.com').hexdigest()

        post_data = {
            'first_name': f_name_sha1,
            'last_name': f_name_sha1,
            'contact_email': email_sha1,
        }

        response = self.client.post('/edit_contacts/', post_data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertContains(response, f_name_sha1)

