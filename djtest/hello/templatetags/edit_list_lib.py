from django import template

register = template.Library()

@register.tag(name='edit_list')
def do_edit_list(parser, token):
    pass
