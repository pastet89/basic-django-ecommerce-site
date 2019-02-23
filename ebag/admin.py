from django.contrib import admin
from .models import Category, Product
from mptt.admin import DraggableMPTTAdmin
from . import forms
# Register your models here.


class MyDraggableMPTTAdmin(DraggableMPTTAdmin):
    form = forms.CategoryForm
    exclude = ('slug',)

class MyModelAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Category, MyDraggableMPTTAdmin)
admin.site.register(Product, MyModelAdmin)
