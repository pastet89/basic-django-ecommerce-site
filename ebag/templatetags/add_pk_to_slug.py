from django import template
from django.conf import settings


register = template.Library()

@register.filter
def add_pk_to_slug(context):
    """
    Changes the category slug, inserting in it the category id:
    something which can't be done during the category creation
    as the id still does not exist at this time. Gets the complete
    node category data with all the fields and returns only the slug.
    :param context: category node from Category.objects.all() 
    :type context: ebag.models.Category
    """
    return context.slug.replace(settings.PK_PLACEHOLDER, str(context.pk))
