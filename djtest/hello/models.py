from django.db import models

class Contacts(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_email = models.CharField(max_length=100)


class HttpReqs(models.Model):

    date = models.DateTimeField()
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=300)
    GET = models.TextField()
    POST = models.TextField()
    cookies = models.TextField()


