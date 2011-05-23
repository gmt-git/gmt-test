from django.contrib import admin
from djtest.hello.models import Contacts, HttpReqs

admin.site.register(Contacts)
admin.site.register(HttpReqs)
