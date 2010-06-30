#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import re
import json
import hashlib
from string import find

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.db import models
from django.test import TestCase, client
from django.template import Template, Context
from django.utils.encoding import force_unicode

from djtest.hello.models import HttpReqs, Contacts, ModelsLog
from djtest.hello.forms import CalendarWidget
from djtest.hello.management.commands import printmodels

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
        email = 'gmt.more@gmail.com'

        post_data = {
            'first_name': f_name_sha1,
            'last_name': f_name_sha1,
            'contact_email': email,
            'birth_date': '1908-02-29' 
        }

        response = self.client.post('/edit_contacts/', post_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/')
        self.assertContains(response, f_name_sha1)


class AuthReqTest(TestCase):

    def setUp(self):
        self.client = client.Client()

    def test_auth_required(self):
        response = self.client.get('/auth_req/edit_contacts/')
        self.assertRedirects(response, '/accounts/login/?next=/auth_req/edit_contacts/')
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get('/auth_req/edit_contacts/')
        self.failUnlessEqual(response.status_code, 200)

class EditContactsFormTest(TestCase):

    def test_edit_contacts_form(self):
        self.client = client.Client()

        f_name_sha1 = hashlib.sha1('Max').hexdigest()
        my_email = 'gmt.more@gmail.com'

        post_data = {
            'first_name': f_name_sha1,
            'last_name': 'Yuzhakov',
            'contact_email': my_email,
            'birth_date': '1908-02-29' 
        }

        # перевірка необхідності авторізації та логін
        response = self.client.get('/edit_contacts_form/')
        self.assertRedirects(response, '/accounts/login/?next=/edit_contacts_form/')
        self.assertTrue(self.client.login(username='admin', password='admin'))
        # перевірка контенту
        response = self.client.get('/edit_contacts_form/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, my_email)
        # перевірка можливості збрерігання змін
        response = self.client.post('/edit_contacts_form/', post_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/')
        self.assertContains(response, f_name_sha1)

    def test_calendar_widget(self):
        self.client = client.Client()
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get('/edit_contacts_form/')
        self.assertContains(response, 'class="vDateField"')

class EditListTagTest(TestCase):

    def test_edit_link(self):
        me = Contacts.objects.get(contact_email='gmt.more@gmail.com')
        ct = ContentType.objects.get_for_model(me)
        # Знаходимо change_url для тестового об'єкту
        change_url = urlresolvers.reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=(me.id,))

        # Тестова модель, яку тег не повинен рендерить
        class TestModel(models.Model):
            testfield = models.CharField()

        tm_inst = TestModel(testfield="hello")

        # Створюємо шаблон для перевірки нового тегу (edit_link),
        # Та контексти для тестовго об'екту, та трьох об'єктів що не повинні рендериться
        t1 = Template('{% load edit_list_lib %}{% edit_link me %}')

        c1 = Context({'me': me})
        c2 = Context({'me': tm_inst})
        c3 = Context({'me': None})
        c4 = Context({'me': 1.5})
        c5 = Context({'nonexistent': me})

        # Рендерінг випадкових обєктів повинен бути відсутнім
        # Якщо помилка у рендерінгу, повиннен сформуватися лінк '/debug/tags/edit_link/d/'
        # останній компонент шляху 'd' -- код помилки
        # при тестуванні останні два сімволи з лінку вирізаємо
        # Бо невідомо, який тест яку помилку видасть
        self.assertEqual(t1.render(c2)[:-2], '/debug/tags/edit_link/')
        self.assertEqual(t1.render(c3)[:-2], '/debug/tags/edit_link/')
        self.assertEqual(t1.render(c4)[:-2], '/debug/tags/edit_link/')

        # Рендерінг повинен давати лінк
        self.assertEqual(t1.render(c1), change_url)

        # Перевіряємо присутність на головній сторінці лінку на редагування контактів в адмінці
        href = u'href="%s"' % change_url
        self.assertContains(client.Client().get(u'/'), href)

        # Перевіряємо що шаблон з помилкою працює як належить
        self.assertContains(client.Client().get(u'/debug/tags/edit_link/3/'), 'Код помилки: 3')
        self.assertContains(client.Client().get(u'/debug/tags/edit_link/3/'), 'тегу: edit_link')

class ModelSignalsTest(TestCase):

    def test_models_signal_handler(self):
        me2 = Contacts(first_name='Maxim', last_name='Yuzhakov',
            contact_email='max@example.com', birth_date='1908-02-29')
        myct = ContentType.objects.get_for_model(me2)

        # Тест на додавання
        logcnt = ModelsLog.objects.filter(content_type=myct.id).count()
        me2.save()
        # Перевіряємо що записів стало на один більше
        self.assertEqual(ModelsLog.objects.filter(content_type=myct.id).count(), logcnt+1)

        # Перевіряємо що останній запис має action_flag 'ADD'
        lastlog = ModelsLog.objects.filter(content_type=myct.id, object_id=me2.pk). \
            order_by('-action_time')[0]
        self.assertEqual(lastlog.action_flag, u'ADD')

        # Тест на зміни
        me2.first_name = 'Max'
        me2.save()
        self.assertEqual(ModelsLog.objects.filter(content_type=myct.id).count(), logcnt+2)

        lastlog = ModelsLog.objects.filter(content_type=myct.id, object_id=me2.pk). \
            order_by('-action_time')[0]
        self.assertEqual(lastlog.action_flag, u'MOD')

        # Тест на видалення
        me2pk = me2.pk
        me2.delete()
        self.assertEqual(ModelsLog.objects.filter(content_type=myct.id).count(), logcnt+3)

        lastlog = ModelsLog.objects.filter(content_type=myct.id, object_id=me2pk). \
            order_by('-action_time')[0]
        self.assertEqual(lastlog.action_flag, u'DEL')


class JQueryFormTest(TestCase):

    def test_xhr_request(self):
        tcl = client.Client()
        # На початку перевіряємо доступність бібліотек
        response = tcl.post('/static_media/js/jquery.js')
        self.failUnlessEqual(response.status_code, 200)
        response = tcl.post('/static_media/js/jquery.form.js')
        self.failUnlessEqual(response.status_code, 200)

        # Авторізація
        response = self.client.get('/edit_contacts_form/')
        self.assertRedirects(response, '/accounts/login/?next=/edit_contacts_form/')
        self.assertTrue(self.client.login(username='admin', password='admin'))

        post_data = {
            'first_name': 'Max',
            'last_name': 'Yuzhakov',
            'contact_email': 'gmt.more@gmail.com',
            'birth_date': '1908-02-29'
        }

        # Відповідь повинна віддавати код 200 та містити vDateField наприклад
        # У всякому разі відповідь повинна отримувати новий вміст форми
        # З помилками валідації, чи ні
        response = self.client.post('/edit_contacts_form/', post_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="vDateField"')
        self.assertNotContains(response, '<head>')

        post_data['birth_date'] = ''

        # У разі невалідних данних відповідь також не повинна містити <head>
        response = self.client.post('/edit_contacts_form/', post_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="vDateField"')
        self.assertNotContains(response, '<head>')


class ListViewTest(TestCase):

    def test_httpreqs_list(self):
        # Генеруємо запити
        tcl = client.Client()
        test_urls = ['/testurl/%d/' % i for i in range(30)]
        resp_list = [tcl.get(test_url) for test_url in test_urls]



__test__ = {"commands": printmodels.handle_test}
