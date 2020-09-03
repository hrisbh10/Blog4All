from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context,**kwargs):
    new_request = context['request'].GET.copy()
    for kwarg in kwargs:
    	if kwarg in new_request:
    		new_request.pop(kwarg)
    new_request.update(kwargs)
    return new_request.urlencode()
