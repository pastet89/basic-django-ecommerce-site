from django.shortcuts import render, redirect
from .models import Category, Product
from django.views.generic import ListView
from django.http import JsonResponse
from .forms import CheckoutForm
from functools import wraps
import json
# Create your views here.


class BaseMixin:
    @staticmethod
    def common_data(request, ctx=None):
        if ctx is None:
            ctx = {}
        ctx['categories'] = Category.objects.all()
        ctx["items_in_cart"] = 0
        if "cart" in request.session:
            ctx["cart"] = [
                item for key, item in request.session["cart"].items()
            ]
            cart_total = sum([
                int(item["quantity"]) * float(item["product_data"]["price"])
                for item in ctx["cart"]
            ])
            ctx["cart_total"] = cart_total
        else:
            ctx["cart"] = []
        ctx["items_in_cart"] = len(ctx["cart"])
        return ctx

    @staticmethod
    def validate_referrer(coming_from):
        def outer_wrapper(function):
            @wraps(function)
            def inner_wrapper(request, *args, **kwargs):
                if coming_from not in str(request.META.get('HTTP_REFERER')):
                    return redirect('home_view')
                return function(request, *args, **kwargs)
            return inner_wrapper
        return outer_wrapper

    @staticmethod
    def verify_cart_not_empty(function):
        @wraps(function)
        def inner_dec(request, *args, **kwargs):
            if "cart" not in request.session:
                return redirect('home_view')
            return function(request, *args, **kwargs)
        return inner_dec


class CategoryView(ListView):
    template_name = 'category.html'
    model = Category

    def get_context_data(self, **kwargs):
        ctx = super(__class__, self).get_context_data(**kwargs)
        ctx['category'] = Category.objects.get(id=self.kwargs["cat_id"])
        ctx['products'] = Product.objects.filter(
            category_id=self.kwargs["cat_id"]
        ).values()
        for product in ctx['products']:
            product_id = str(product["id"])
            session = self.request.session
            if ("cart" not in session or product_id not in session["cart"]):
                product["quantity"] = 1
            else:
                product["quantity"] = session["cart"][product_id]["quantity"]
        return BaseMixin.common_data(self.request, ctx)


def home_view(request):
    return render(request, "home.html", BaseMixin.common_data(request))


@BaseMixin.verify_cart_not_empty
def cart_view(request):
    return render(request, "cart.html", BaseMixin.common_data(request))


@BaseMixin.validate_referrer('/checkout/')
def thank_you_view(request):
    return render(request, "thank-you.html", BaseMixin.common_data(request))


@BaseMixin.verify_cart_not_empty
@BaseMixin.validate_referrer('/cart/')
def checkout_view(request):
    form = CheckoutForm()
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            del request.session["cart"]
            request.session.save()
            return redirect("thank_you_view")
    ctx = {
        "form": form
    }
    return render(
        request,
        "checkout.html",
        BaseMixin.common_data(request, ctx)
    )


def ajax_session_cart(request):
    success = 1
    if "cart" not in request.session:
        request.session["cart"] = {}
    for item in json.loads(request.POST["items"]):
        product_id = item["product_id"]
        quantity = item["quantity"]
        fields = (product_id, quantity)
        if any(f.isdigit() is not True for f in fields):
            success = 0
        elif int(quantity) > 0:
            product_data = {
                k: str(v) for k, v in
                Product.objects.filter(id=product_id).values()[0].items()
            }
            request.session["cart"].update(
                {product_id: {
                    "quantity": quantity,
                    "product_data": product_data
                    }
                 }
            )
        elif int(quantity) == 0:
            try:
                del request.session["cart"][product_id]
            except KeyError:
                pass
    request.session.save()
    items_in_cart = len(request.session["cart"])
    if items_in_cart < 1:
        del request.session["cart"]
        request.session.save()
    try:
        cart = request.session["cart"]
    except KeyError:
        cart = {}
    data = {
        'success': success,
        'items_in_cart': items_in_cart,
        'cart': cart
    }
    return JsonResponse(data)
