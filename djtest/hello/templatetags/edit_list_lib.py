#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry

register = template.Library()

class EditListNode(template.Node):

    def __init__(self, obj, test):
        self.obj = template.Variable(obj)
        self.test = test
        self.result = ''

    def render(self, context):
        try:
            obj_inst = self.obj.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        try:
            obj_id = obj_inst.pk
            ct_id = ContentType.objects.get_for_model(obj_inst).pk
        except AttributeError:
            obj_id = None
            ct_id = None

        qs = LogEntry.objects.filter(content_type=ct_id, object_id=obj_id)
        if self.test:
            self.result = ','.join(qs.values_list('change_message', flat=True))
        else:
            if qs.count() > 0:
                self.result += u'<table><caption>Зміни %s</caption><tr>' % qs[0].object_repr
                self.result += u'<th>%s</th><th>%s</th><th>%s</th><th>%s</th>' % \
                    ('action_time', 'user', 'content_type', 'object_repr')
                self.result += u'<th>%s</th><th>%s</th></tr>' % ('action_flag', 'change_message')

                for r in qs:
                    self.result += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % \
                        (r.action_time, r.user, r.content_type, r.object_repr)
                    self.result += u'<td>%s</td><td>%s</td></tr>' % (r.action_flag, r.change_message)

                self.result += u'</table>'

        return self.result

@register.tag(name='edit_list')
def do_edit_list(parser, token):
    tag_args = token.split_contents()
    if len(tag_args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % tag_args[0]

    if len(tag_args) > 2:
        return EditListNode(obj=tag_args[1], test=True)
    else:
        return EditListNode(obj=tag_args[1], test=False)
