from django.contrib import admin
from .models import Category, Product
from mptt.admin import DraggableMPTTAdmin
from . import forms
from django.db.models import F
# Register your models here.


class CategoryDraggableMPTTAdmin(DraggableMPTTAdmin):
    form = forms.CategoryForm
    exclude = ('slug',)

class ProductModelAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(rght=F('lft') + 1)
        return super(__class__, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category, CategoryDraggableMPTTAdmin)
admin.site.register(Product, ProductModelAdmin)
