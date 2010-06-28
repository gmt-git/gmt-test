#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import NoArgsCommand, CommandError

class Command(NoArgsCommand):
    help = 'Print project models and object count'

    def handle_noargs(self, *args, **options):
        sys.stdout.write(get_models_and_count())

def get_models_and_count():
    result = 'Project models:\n\n'
    for ct in ContentType.objects.order_by('id'):
        result += ct.app_label + '.' + ct.model + ' count=' + str(ct.model_class().objects.count()) + '\n'
    result += '\nTotal models count: %d' % ContentType.objects.all().count()
    return result

def handle_test():
    """
    >>> from hello.management.commands.printmodels import Command, get_models_and_count
    >>> c = Command()
    >>> c.handle_noargs()
    Project models:
    ...
    hello.contacts count=1
    hello.httpreqs count=0
    ...
    Total models count...
    """
