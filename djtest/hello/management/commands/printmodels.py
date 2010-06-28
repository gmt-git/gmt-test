#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import NoArgsCommand, CommandError

class Command(NoArgsCommand):
    help = 'Команда друкує всі моделі проекту'

    def handle_noargs(self, *args, **options):
        sys.stdout.write(get_models_and_count())

def get_models_and_count():
    result = ''
    for ct in ContentType.objects.order_by('id'):
        result += ct.app_label + '.' + ct.model + ' count=' + str(ct.model_class().objects.count()) + '\n'
    return result

def handle_test():
    """
    >>> from hello.management.commands.printmodels import Command, get_models_and_count
    >>> c = Command()
    >>> c.handle_noargs()
    admin.logentry count=0
    auth.permission count=30
    auth.group count=0
    auth.user count=1
    auth.message count=0
    contenttypes.contenttype count=10
    sessions.session count=0
    sites.site count=1
    hello.contacts count=1
    hello.httpreqs count=0
    """
