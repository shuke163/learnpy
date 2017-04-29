import copy

from django.template import Node, Variable, VariableDoesNotExist, TemplateSyntaxError
from django.template.defaultfilters import register, stringfilter


class VarNode(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        try:
            value = Variable(self.value).resolve(context=context)
        except VariableDoesNotExist:
            value = ""
        context[self.name] = copy.deepcopy(value)
        return ''


@register.tag
def setvar(parser, token):
    parts = token.split_contents()
    if len(parts) < 4:
        raise TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return VarNode(parts[1], parts[3])


@register.filter
@stringfilter
def startswith(value, arg):
    return value.startswith(arg)


@register.filter
def active(value, arg):
    for first in value:
        first['active'] = 0
        for second in first['sub']:
            if arg.startswith(second['url']):
                second['active'] = 1
                first['active'] = 1
            else:
                second['active'] = 0
    return value
