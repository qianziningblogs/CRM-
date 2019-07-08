from django import template
from django.urls import reverse
from django.http.request import QueryDict

register = template.Library()

@register.simple_tag
def reverse_url(request,name,*args,**kwargs):
    next = request.get_full_path()

    qd = QueryDict(mutable=True)
    qd['next'] = next
    base_url = reverse(name, args=args,kwargs=kwargs)

    return '{}?{}'.format(base_url,qd.urlencode())