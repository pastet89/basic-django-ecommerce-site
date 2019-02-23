from django.conf import settings
from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
    def clean_name(self):
        name = self.cleaned_data["name"]
        if settings.PK_PLACEHOLDER in name:
            raise forms.ValidationError(f"{settings.PK_PLACEHOLDER} is a reserved "
                                         "placeholder, you can't use it in the category name.")
        return name
