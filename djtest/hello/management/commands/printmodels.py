#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import NoArgsCommand, CommandError

class Command(NoArgsCommand):
    help = 'Команда друкує всі моделі проекту'

    def handle_noargs(self, *args, **options):
        sys.stdout.write('Test Error')

def get_models_and_count():
    result = {}
    for ct in ContentType.objects.order_by('id'):
        result[ct.app_label+'.'+ct.model] = ct.model_class().objects.count()
    return result

def handle_test():
    """
    >>> from hello.management.commands.printmodels import Command, get_models_and_count
    >>> c = Command()
    >>> c.handle_noargs()
    test OK
    """

