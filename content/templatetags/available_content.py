from django import template
from django.urls import reverse

from ..models import Content


register = template.Library()


@register.assignment_tag
def available_content():
    sections = []

    for type in ['projects', 'events', 'works', 'texts']:
        if Content.objects.filter(type__name=type, published=True).exists():
            sections.append([
                reverse('works'),
                type.capitalize()
            ])
    return sections
