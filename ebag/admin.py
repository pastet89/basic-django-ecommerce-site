from django.contrib import admin
from .models import Category, Product
from mptt.admin import DraggableMPTTAdmin
from . import forms
from django.db.models import F
# Register your models here.


class CategoryDraggableMPTTAdmin(DraggableMPTTAdmin):
    """
    Applies the Django-MPTT draggable widget to the categories
    so that their levels can be viewd and changed with a single
    mouse move.
    """
    form = forms.CategoryForm


class ProductModelAdmin(admin.ModelAdmin):
    """
    Excludes the slug field from the form as it should be
    generated automatically. Filters the categories in a way
    that ensures that a product can be put only in a leaf (bottom)
    node and not in a category which contains subcategories.
    """

    exclude = ('slug',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Filters the category queryset so that only leaf nodes are selected.
        """

        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(rght=F('lft') + 1)
        return super(__class__, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


admin.site.register(Category, CategoryDraggableMPTTAdmin)
admin.site.register(Product, ProductModelAdmin)
