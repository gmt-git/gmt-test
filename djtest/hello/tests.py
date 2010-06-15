import os
import json
from django.conf import settings
from django.test import TestCase, client

class HelloTest(TestCase):

    def setUp(self):
        self.client = client.Client()

    def test_homepage_request(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)

    def test_response_context(self):
        initial_data_path = os.path.join(settings.PROJ_ROOT, 'hello/fixtures/initial_data.json')
        initial_data_str = open(initial_data_path).read()
        data_list = json.loads(initial_data_str)

        first_name = data_list[0]['fields']['first_name']
        last_name = data_list[0]['fields']['last_name']
        contact_email = data_list[0]['fields']['contact_email']

        response = self.client.get('/')

        self.failUnlessEqual(response.context['first_name'], first_name)
        self.failUnlessEqual(response.context['last_name'], last_name)
        self.failUnlessEqual(response.context['contact_email'], contact_email)
