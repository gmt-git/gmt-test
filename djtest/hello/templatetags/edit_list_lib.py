from django import template

register = template.Library()

class EditListNode(template.Node):
    pass

@register.tag(name='edit_list')
def do_edit_list(parser, token):
    tag_args = token.split_contents()
    if len(tag_args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % tag_args[0]

    if len(tag_args) > 2:
        return EditListNode(obj=tag_args[1], test=True)
    else:
        return EditListNode(obj=tag_args[1], test=False)
