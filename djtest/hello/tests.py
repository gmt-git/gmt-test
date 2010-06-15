from django.test import TestCase, client

class HelloTest(TestCase):

    def setUp(self):
        self.client = client.Client()

    def test_homepage_request(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
