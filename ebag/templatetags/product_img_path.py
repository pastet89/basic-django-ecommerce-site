from django import template
from django.conf import settings


register = template.Library()

@register.filter
def product_img_path(img_path):
    return img_path.split(settings.STATIC_URL)[-1]

