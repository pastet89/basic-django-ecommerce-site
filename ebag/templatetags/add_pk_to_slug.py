from django import template
from django.conf import settings


register = template.Library()

@register.filter
def add_pk_to_slug(context):
    return context.slug.replace(settings.PK_PLACEHOLDER, str(context.pk))
