from builtins import object
from django.template import Library
from django.template.base import Node, NodeList, VariableDoesNotExist
from django.template.defaulttags import TemplateLiteral
from django_simple_rbac.helpers import is_allowed


register = Library()


class TemplateIfIsAllowedParser(object):

    def __init__(self, parser, tokens):
        self.template_parser = parser
        self.tokens = tokens

    def parse(self):
        operation = TemplateLiteral(self.template_parser.compile_filter(self.tokens[0]), self.tokens[0])
        resource = TemplateLiteral(self.template_parser.compile_filter(self.tokens[1]), self.tokens[1])
        return operation, resource


class IfIsAllowedNode(Node):

    def __init__(self, checks_nodelists):
        self.checks_nodelists = checks_nodelists

    def __repr__(self):
        return "<IfIsAllowedNode>"

    def __iter__(self):
        for _, nodelist in self.checks_nodelists:
            for node in nodelist:
                yield node

    @property
    def nodelist(self):
        return NodeList(node for _, nodelist in self.checks_nodelists for node in nodelist)

    def render(self, context):
        for check, nodelist in self.checks_nodelists:
            context['authority'] = None
            if check is not None:           # ifisallowed / elifisallowed clause
                try:
                    operation, resource = check
                    match = is_allowed(context['request'], operation.eval(context), resource.eval(context))

                    # add authority to template context
                    context['authority'] = match.authority
                except VariableDoesNotExist:
                    match = None
            else:                               # else clause
                match = True

            if match:
                return nodelist.render(context)

        return ''


@register.tag('ifisallowed')
def do_if_is_allowed(parser, token):
    """
    The ``{% ifisallowed %}`` tag evaluates a variable, and if that variable is "true"
    (i.e., exists, is not empty, and is not a false boolean value), the
    contents of the block are output:

    ::

        {% ifisallowed 'update' member %}
            You can edit this member !
        {% else %}
            Sorry, you can't update this member.
        {% endifisallowed %}
    """

    # {% ifisallowed ... %}
    bits = token.split_contents()[1:3]
    check = TemplateIfIsAllowedParser(parser, bits).parse()
    nodelist = parser.parse(('elifisallowed', 'else', 'endifisallowed'))
    checks_nodelists = [(check, nodelist)]
    token = parser.next_token()

    # {% elifisallowed ... %} (repeatable)
    while token.contents.startswith('elifisallowed'):
        bits = token.split_contents()[1:3]
        check = TemplateIfIsAllowedParser(parser, bits).parse()
        nodelist = parser.parse(('elifisallowed', 'else', 'endifisallowed'))
        checks_nodelists.append((check, nodelist))
        token = parser.next_token()

    # {% else %} (optional)
    if token.contents == 'else':
        nodelist = parser.parse(('endifisallowed',))
        checks_nodelists.append((None, nodelist))
        token = parser.next_token()

    # {% endifisallowed %}
    assert token.contents == 'endifisallowed'

    return IfIsAllowedNode(checks_nodelists)


@register.simple_tag(takes_context=True)
def isallowed(context, operation, resource, authority=None):
    """
    Useful when you want to store ACL result in a variable to be tested with other parameters. For example :

    {% isallowed "my_operation" my_resource as can_do_operation %}
    {% if my_resource.some_boolean or can_do_operation %}
        Display stuff
    {% endif %}
    """
    authorities = [authority] if authority else None
    return is_allowed(context['request'], operation, resource, authorities)
