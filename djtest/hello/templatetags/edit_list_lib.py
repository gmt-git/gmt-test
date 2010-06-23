from django import template

register = template.Library()

class EditListNode(template.Node):
    pass

@register.tag(name='edit_list')
def do_edit_list(parser, token):
    return EditListNode()
