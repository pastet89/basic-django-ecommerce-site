from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.views import View
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict
# Create your views here.

class BaseMixin:
    @staticmethod
    def common_data(request, ctx=None):
        if ctx is None:
            ctx = {}
        ctx['categories'] = Category.objects.all()
        ctx["items_in_cart"] = 0
        if "cart" in request.session:
            ctx["items_in_cart"] = len(request.session["cart"])
        return ctx

def home_view(request):
    return render(request, "home.html", BaseMixin.common_data(request))

def cart_view(request):
    ctx = {}
    if "cart" not in request.session:
        ctx["cart"] = {} 
    else:
        ctx["cart"] = [item for key, item in request.session["cart"].items()]
    return render(request, "cart.html", BaseMixin.common_data(request, ctx))

def update_cart():
    pass

def add_to_cart(request):
    success = 1
    if "cart" not in request.session:
        request.session["cart"] = dict()
    request_fields = (request.POST["product_id"], request.POST["quantity"])
    if any(f.isdigit() is not True for f in request_fields):
        success = 0
    elif int(request.POST["quantity"]) > 0:
        product_data = {k:str(v) for k, v in Product.objects.filter(id=request.POST["product_id"]).values()[0].items()}
        request.session["cart"].update(
            {request.POST["product_id"]: {
                "quantity": request.POST["quantity"],
                "product_data": product_data
                }
            }
        )
    elif int(request.POST["quantity"]) == 0:
        try:
            del request.session["cart"][request.POST["product_id"]]
        except KeyError:
            pass
    request.session.save()
    data = {
        'success': success,
        'items_in_cart': len(request.session["cart"]),
        'cart': request.session["cart"],
    }
    return JsonResponse(data)

class CategoryView(ListView):
    template_name = 'category.html'
    model = Category
        
    def get_context_data(self, **kwargs):
        ctx = super(__class__, self).get_context_data(**kwargs)
        ctx['category'] = Category.objects.get(id=self.kwargs["cat_id"])
        ctx['products'] = Product.objects.filter(category_id=self.kwargs["cat_id"])
        return BaseMixin.common_data(self.request, ctx)

    """def clear_image_path(self, product_dict):
        product_dict.image.name = product_dict.image.name.split(settings.STATIC_URL)[-1]
        return product_dict"""
