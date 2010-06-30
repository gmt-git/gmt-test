#!/usr/bin/python
# -*- coding: utf-8 -*- 

from django import template
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers

register = template.Library()

class EditLinkNode(template.Node):

    def __init__(self, obj):
        self.obj = template.Variable(obj)
        self.result = '/debug/tags/%s/%d/'

    def render(self, context):
        try:
            obj_inst = self.obj.resolve(context)
        except template.VariableDoesNotExist:
            return self.result % ('edit_link', 1)

        try:
            obj_id = obj_inst.pk
            ct = ContentType.objects.get_for_model(obj_inst)
        except AttributeError:
            return self.result % ('edit_link', 2)

        if not obj_id:
            return self.result % ('edit_link', 3)

        return urlresolvers.reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=(obj_id,))

@register.tag(name='edit_link')
def do_edit_link(parser, token):
    tag_args = token.split_contents()
    if len(tag_args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % tag_args[0]

    return EditLinkNode(obj=tag_args[1])
