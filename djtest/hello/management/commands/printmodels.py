#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys
from django.core.management.base import NoArgsCommand, CommandError

class Command(NoArgsCommand):
    help = 'Команда друкує всі моделі проекту'

    def handle_noargs(self, *args, **options):
        sys.stdout.write('Test Error')

def handle_test():
    """
    >>> from hello.management.commands.printmodels import Command
    >>> c = Command()
    >>> c.handle_noargs()
    test OK
    """

