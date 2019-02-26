from django.conf import settings
from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    """
    The admin form for creation/update of categories.
    """

    class Meta:
        model = Category
        fields = '__all__'

    def clean_name(self):
        """
        Doesn't allow the PK_PLACEHOLDER specified in the settings
        to be included in the category name as it has a special function.
        It will be later replaced in the slug url with the category id.
        The slug can not be created with id during the
        category creation as the object still doesn't exist so is not assigned
        any id, hence the need of the placeholder.
        """
        name = self.cleaned_data["name"]
        if settings.PK_PLACEHOLDER in name:
            raise forms.ValidationError(f"{settings.PK_PLACEHOLDER} is a "
                                        "reserved placeholder, you can't "
                                        "use it in the category name.")
        return name


class CheckoutForm(forms.Form):
    """
    Dummy Checkout form without performed action on successful validation,
    just checks for field errors.
    """

    COUNTRIES = (
        ('', 'Choose a country'),
        ('1', 'Bulgaria'),
        ('2', 'Serbia'),
        ('3', 'USA')
    )
    country = forms.ChoiceField(label='Country',
                                widget=forms.Select(
                                    attrs={
                                        'class': 'form-control'
                                    }),
                                choices=COUNTRIES
                                )
    first_name = forms.CharField(label='First Name',
                                 max_length=30,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                     })
                                 )
    last_name = forms.CharField(label='Last Name',
                                max_length=30,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control'
                                     })
                                )
    company_name = forms.CharField(label='Company Name',
                                   required=False,
                                   max_length=100,
                                   widget=forms.TextInput(
                                      attrs={
                                        'class': 'form-control'
                                      })
                                   )
    address_1 = forms.CharField(label='Address',
                                max_length=100,
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder': 'Street Address',
                                        'class': 'form-control'
                                    })
                                )
    address_2 = forms.CharField(max_length=200,
                                required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder': 'Apartment, suite, etc.'
                                    })
                                )
    state_region = forms.CharField(label='State / Region',
                                   max_length=50,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control'
                                       })
                                   )
    post_code = forms.IntegerField(label='Post code',
                                   widget=forms.NumberInput(
                                        attrs={
                                            'class': 'form-control'
                                        })
                                   )
    email = forms.EmailField(label='Email Address',
                             max_length=50,
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control'
                                 })
                             )
    phone = forms.IntegerField(label='Phone',
                               widget=forms.NumberInput(
                                   attrs={
                                       'class': 'form-control'
                                    })
                               )
    order_notes = forms.CharField(label='Additional notes',
                                  required=False,
                                  widget=forms.Textarea(
                                      attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Any special notes?',
                                          'cols': 30,
                                          'rows': 5
                                        })
                                  )
