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

        if self.test:
            self.result = ','.join( \
                LogEntry.objects.filter(content_type=ct_id, object_id=obj_id). \
                values_list('change_message', flat=True)
            )

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
