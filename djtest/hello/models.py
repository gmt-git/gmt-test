#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType

def modelslog_save_handler(sender, **kwargs):
    excl_ct = ContentType.objects.get_for_model(ModelsLog)
    sender_ct = ContentType.objects.get_for_model(sender)
    if sender_ct == excl_ct:
        return

def modelslog_delete_handler(sender, **kwargs):
    excl_ct = ContentType.objects.get_for_model(ModelsLog)
    sender_ct = ContentType.objects.get_for_model(sender)
    if sender_ct == excl_ct:
        return

post_save.connect(modelslog_save_handler)
post_delete.connect(modelslog_delete_handler)

class Contacts(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_email = models.CharField(max_length=100)
    birth_date = models.DateField()


class HttpReqs(models.Model):

    date = models.DateTimeField()
    method = models.CharField(max_length=10)
    full_path = models.CharField(max_length=300)
    meta = models.TextField()
    cookies = models.TextField()


class ModelsLog(models.Model):

    action_time = models.DateTimeField()
    content_type = models.ForeignKey(ContentType)
    content_type = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=300)
    action_flag = models.CharField(max_length=5)
