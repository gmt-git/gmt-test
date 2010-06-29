#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.core import urlresolvers
from django.template.loader import render_to_string

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
            return ''

        qs = LogEntry.objects.filter(content_type=ct_id, object_id=obj_id)

        if qs.count() == 0:
            return ''

        if self.test:
            self.result = ','.join(qs.values_list('change_message', flat=True))
        else:
            fields = ['action_time', 'user', 'content_type',
                'object_repr', 'action_flag', 'change_message']

            # Список списків де рядки це рядки QuerySet, а стовпці задані fields
            data = [[getattr(le_inst, f, '') for f in fields] for le_inst in qs]

            self.result = render_to_string('edit_list_lib.html',
                {
                    'caption': u'Зміни %s' % qs[0].object_repr,
                    'fields': fields,
                    'data': data
                })

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


class EditLinkNode(template.Node):

    def __init__(self, obj):
        self.obj = template.Variable(obj)
        self.result = ''

    def render(self, context):
        try:
            obj_inst = self.obj.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        try:
            obj_id = obj_inst.pk
            ct = ContentType.objects.get_for_model(obj_inst)
        except AttributeError:
            return ''

        if not obj_id:
            return ''

        return urlresolvers.reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=(obj_id,))

@register.tag(name='edit_link')
def do_edit_link(parser, token):
    tag_args = token.split_contents()
    if len(tag_args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % tag_args[0]

    return EditLinkNode(obj=tag_args[1])
