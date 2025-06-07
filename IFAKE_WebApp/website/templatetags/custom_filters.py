from django import template

register = template.Library()

@register.filter(name='unslugify')
def unslugify(value):
    """
    Substitui underscores por espaços em uma string.
    """
    return value.replace('_', ' ')