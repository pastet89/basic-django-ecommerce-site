"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ebag import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/<int:cat_id>/<slug:cat_name>/',
         views.CategoryView.as_view(),
         name='category'
         ),
    path('cart/add/', views.ajax_session_cart, name='add_to_cart'),
    path('cart/update/', views.ajax_session_cart, name='update_cart'),
    path('', views.home_view, name='home_view'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('thank-you/', views.thank_you_view, name='thank_you_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
