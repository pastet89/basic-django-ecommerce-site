import os
import json
import unittest
from datetime import datetime
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import reverse
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib import admin
from .templatetags import add_pk_to_slug
from .models import Category, Product
from .forms import CategoryForm, CheckoutForm
from .admin import CategoryDraggableMPTTAdmin, ProductModelAdmin
from . import views
from mptt.admin import DraggableMPTTAdmin
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.


class TestingHelper(object):
    """
    Contains helper methods, used on many places
    by other classes.
    """
    def create_cat_and_product(self):
        """
        Creates a testing category and a product in this category.
        Uploads a test product image.
        """
        test_image_src = settings.MEDIA_ROOT + os.sep + "test-img.png"
        if not os.path.isfile(test_image_src):
            raise unittest.SkipTest("Test image for upload missing!")
        self.cat = Category.objects.create(name="test-cat")
        test_image_upload = SimpleUploadedFile(
            name=test_image_src,
            content=open(test_image_src, 'rb').read(),
            content_type='image/png'
        )
        product_data = {
            "name": "Honey",
            "category":  self.cat,
            "description": "Honey is good",
            "price": 1.22,
            "image": test_image_upload,
        }
        self.product = Product.objects.create(**product_data)
        self.product_data = product_data

    def delete_product_image(self):
        """
        Deletes the uploaded by create_cat_and_product() product image.
        """
        self.product.image.delete()


##############################
#     Template tags tests
#############################


class TemplateTagsTestCase(TestCase):
    """
    Tests for the custom template tags
    """

    def setUp(self):
        Category.objects.create()
        self.category_nodes = Category.objects.all()[:1]

    def test_add_pk_to_slug(self):
        """
        Tests add_pk_to_slug() in templatetags/add_pk_to_slug.py
        """
        func_res = add_pk_to_slug.add_pk_to_slug(self.category_nodes[0])
        expected_res = self.category_nodes[0].slug.replace(
            settings.PK_PLACEHOLDER,
            str(self.category_nodes[0].pk)
        )
        self.assertEqual(expected_res, func_res)


##############################
#        Admin tests
#############################


class CategoryDraggableMPTTAdminTestCase(TestCase):
    def test_category_model_admin(self):
        """
        Tests if the ModelAdmin uses the draggable Django-MPTT widget.
        """
        self.assertIn(DraggableMPTTAdmin, CategoryDraggableMPTTAdmin.__bases__)

    def test_model_admin_exclude_fields(self):
        """
        Tests if the ModelAdmin excludes the category slug field
        which should be auto-generated.
        """
        model_admin_obj = CategoryDraggableMPTTAdmin(
            model=Product,
            admin_site=admin.AdminSite()
        )
        self.assertTrue(hasattr(model_admin_obj, "exclude"))
        self.assertEqual(list(model_admin_obj.exclude), ["slug"])

class ProductModelAdminTestCase(TestCase, TestingHelper):
    def setUp(self):
        """
        Creates one Product and two Category objects - on of the categories
        can have products (is leaf node) and the other can't.
        """
        self.create_cat_and_product()
        self.cat_no_leaf_node = Category.objects.create(
            name="name",
            parent=self.cat,
            slug="slug_name"
        )

    def test_limit_categories(self):
        """
        Tests if the ModelAdmin filters the categories in the dropdown
        so products can be added only to leaf nodes.
        """
        model_admin_obj = ProductModelAdmin(
            model=Product,
            admin_site=admin.AdminSite()
        )
        category_field = model_admin_obj.formfield_for_foreignkey(
            Product.category.field, None
        )
        self.assertEqual(1, len(category_field.queryset.values_list()))
        self.assertEqual(1, category_field.queryset.values()[0]['rght'] -
                         category_field.queryset.values()[0]['lft']
                         )

    def tearDown(self):
        """
        Deletes the uploaded test image
        """
        self.product.image.delete()


##############################
#        Forms tests
#############################


class CheckoutFormTestCase(TestCase):
    """
    Checks the validation of the Checkout form
    """

    def test_valid_data(self):
        form = CheckoutForm({
            'country': "1",
            'first_name': "John",
            'last_name': "Smith",
            'company_name': "Apple Inc.",
            'address_1': "Paris str. 5",
            'address_2': "floor 118",
            'post_code': "1234",
            'phone': "088998877",
            'state_region': "Catalonia",
            'email': "leela@example.com",
            'order_notes': "Some notes",
        })
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        required_err = 'This field is required.'
        form = CheckoutForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'country': [required_err],
            'first_name': [required_err],
            'last_name': [required_err],
            'address_1': [required_err],
            'post_code': [required_err],
            'phone': [required_err],
            'state_region': [required_err],
            'email': [required_err],
        })


class CategoryFormTestCase(TestCase):
    """
    Tests the form creating/updating categories from the admin app.
    """

    def test_valid_data(self):
        cat_name = "Test category"
        form = CategoryForm({
            'name': cat_name,
            'parent': None,
        })
        self.assertTrue(form.is_valid())
        cat = form.save()
        self.assertEqual(cat.name, cat_name)
        self.assertEqual(cat.parent, None)
        self.assertIsInstance(cat.last_update, datetime)
        self.assertEqual(cat.slug, "/".join([
            slugify(CategoryForm._meta.model.__name__.lower()),
            settings.PK_PLACEHOLDER,
            slugify(cat.name)
        ]))

    def test_pk_placeholder_error(self):
        """
        Tests if the forms prevents the PK_PLACEHOLDER
        to be included in the category name.
        """
        form = CategoryForm({
            'name':  settings.PK_PLACEHOLDER,
            'parent': None,
        })
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        required_err = 'This field is required.'
        form = CategoryForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': [required_err],
        })


##############################
#        Models tests
#############################


class ProductTestCase(TestCase, TestingHelper):
    def test_string_representation(self):
        product = Product(name="Milk")
        self.assertEqual(str(product), product.name)

    def test_model_save_fields(self):
        """
        Tests the model fields after model saving
        and tests if the image is uploaded.
        """
        self.create_cat_and_product()
        product = self.product
        product.save()
        uploaded_img = settings.MEDIA_ROOT + os.sep + str(product.image)

        self.assertEqual(product.name, "Honey")
        self.assertIsInstance(product.name, str)
        self.assertIsInstance(product.category, Category)
        self.assertEqual(product.description, "Honey is good")
        self.assertIsInstance(product.description, str)
        self.assertEqual(product.price, self.product_data["price"])
        self.assertIsInstance(
            product.image,
            models.fields.files.ImageFieldFile
        )
        self.assertTrue(os.path.isfile(uploaded_img))
        product.image.delete()


class CategoryTestCase(TestCase):
    def test_string_representation(self):
        cat = Category(name="Milk")
        self.assertEqual(str(cat), cat.name)

    def test_parent_category_options(self):
        """
        Tests if category can be created both
        with parent category and non parent category.
        """
        parents = {
            None: None,
            Category: Category.objects.create(),
        }
        for instance, parent in parents.items():
            cat = Category(**{
                "name": "Dairy",
                "parent": parent,
            })
            cat.save()
            if instance is not None:
                self.assertIsInstance(cat.parent, instance)
            else:
                self.assertIs(cat.parent, None)


##############################
#        Views tests
#############################


class GeneralContextMixinTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {}
        self.cat = Category.objects.create()

    def test_categories_in_common_data(self):
        """
        Test if common_data() returns as a dictionary
        the stored categories in the DB.
        """
        common_data = views.GeneralContextMixin.common_data(self.request)
        self.assertIsInstance(common_data, dict)
        self.assertTrue("categories" in common_data)
        self.assertEqual(len(common_data["categories"]), 1)
        self.assertEqual(
            common_data["categories"].values()[0]["id"],
            self.cat.pk
        )

    def test_common_data_empty_cart(self):
        """
        Test if common_data() returns proper data when there
        are no items in the cart stored in the session.
        """
        common_data = views.GeneralContextMixin.common_data(self.request)
        self.assertIsInstance(common_data, dict)
        self.assertEqual(common_data["items_in_cart"], 0)

    def test_common_data_non_empty_cart(self):
        """
        Test if common_data() returns proper data when there
        are items in the cart stored in the session.
        """
        quantity = 2
        price = 4.99
        self.request.session = {
            "cart": {
                "5": {
                    "quantity": quantity,
                    "product_data": {
                        "id": 1,
                        "price": price,
                    }
                }
            }
        }
        common_data = views.GeneralContextMixin.common_data(self.request)
        self.assertIsInstance(common_data, dict)
        self.assertEqual(
            common_data["cart"],
            [self.request.session["cart"]["5"]]
        )
        self.assertEqual(common_data["items_in_cart"], 1)
        self.assertEqual(common_data["cart_total"], quantity * price)

    def test_common_data_add_to_ctx_param(self):
        """
        Test if common_data() includes in the returned data a
        dictionary, passed as a second parameter.
        """

        my_dict = {
            "key": "val"
        }
        common_data = views.GeneralContextMixin.common_data(
            self.request,
            my_dict
        )
        self.assertIsInstance(common_data, dict)
        self.assertTrue("categories" in common_data)
        self.assertTrue("items_in_cart" in common_data)
        self.assertEqual(common_data["key"], "val")


class FunctionBasedViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {}

    def test_home_view(self):
        response = views.home_view(self.request)
        self.assertEqual(response.status_code, 200)

    def test_cart_view_empty_cart(self):
        """
        Test if cart_view redirects to home_view
        if the cart is empty
        """
        response = views.cart_view(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home_view"))

    def test_cart_view_non_empty_cart(self):
        """
        Test if cart_view loads successfully
        if the cart is not empty
        """
        self.request.session = {"cart": {}}
        response = views.cart_view(self.request)
        self.assertEqual(response.status_code, 200)

    def test_checkout_view_empty_cart_bad_refferer(self):
        """
        Test if checkout_view redirects to home_view
        if the cart is empty and the user is not coming
        from /cart/
        """
        response = views.checkout_view(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home_view"))

    def test_checkout_view_empty_cart(self):
        """
        Test if checkout_view redirects to home_view
        if the user is coming from /cart/, but the cart
        is empty
        """
        response = views.checkout_view(self.request)
        self.request.META["HTTP_REFERER"] = '/cart/'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home_view"))

    def test_checkout_view_non_valid_referrer(self):
        """
        Test if checkout_view redirects to home_view if
        the cart is not empty, but user is not coming from
        /cart/
        """
        self.request.session = {"cart": {}}
        response = views.checkout_view(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home_view"))

    def test_checkout_view_non_empty_cart_valid_referrer(self):
        """
        Test if checkout_view loads successfully
        if the cart is not empty and the user is coming
        from /cart/
        """
        self.request.session = {"cart": {}}
        self.request.META["HTTP_REFERER"] = '/cart/'
        response = views.checkout_view(self.request)
        self.assertEqual(response.status_code, 200)

    def test_thank_you_view_valid_referrer(self):
        """
        Test if thank_you view loads successfully
        if the user is coming from /checkout/
        """
        self.request.META["HTTP_REFERER"] = '/checkout/'
        response = views.thank_you_view(self.request)
        self.assertEqual(response.status_code, 200)

    def test_thank_you_view_bad_referrer(self):
        """
        Test if thank_you view redirects to home_view
        if the user is not coming from /checkout/
        """
        response = views.thank_you_view(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home_view"))


class CategoryViewTestCase(TestCase, TestingHelper):
    def setUp(self):
        self.create_cat_and_product()
        self.client = Client()
        self.factory = RequestFactory()
        self.view_url = "/" + \
            self.cat.slug.replace(settings.PK_PLACEHOLDER,
                                  str(self.cat.pk)) + "/"
        self.request = self.factory.get(self.view_url)

    def test_category_view(self):
        try:
            # If setup_test_environment haven't been called previously this
            # will produce an AttributeError.
            teardown_test_environment()
        except AttributeError:
            pass
        setup_test_environment()
        quantity = 2
        self.request.session = {
            "cart": {
                "5": {
                    "quantity": quantity,
                    "product_data": {
                        "id": 1,
                        "price": 5,
                    }
                }
            }
        }
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("categories" in response.context)
        self.assertTrue("products" in response.context)
        self.assertEqual(response.context["categories"].values()[
                         0]["id"], self.cat.pk)
        self.assertEqual(response.context["products"].values()[
                         0]["id"], self.product.pk)

    def tearDown(self):
        self.product.image.delete()


class AJAXSessionCartTestCase(TestCase, TestingHelper):

    def setUp(self):
        self.create_cat_and_product()
        self.client = Client()
        self.factory = RequestFactory()
        self.general_request = self.factory.post(reverse("add_to_cart"), {
            "items": json.dumps([{
                "product_id": "1",
                "quantity": "1",
            }])
        })
        self.view = self.helper_setup_view(
            views.AJAXSessionCart(), self.general_request)

    def helper_setup_view(self, view, request, *args, **kwargs):
        """Mimic as_view() returned callable, but returns view instance.
        args and kwargs are the same you would pass to ``reverse()``

        Also sets a view session taking it from the Client() instance -
        needed for testing internal (say, helper) View class methods.

        :param view: The Class view instance
        :type var: Any of the Django view classes or any inherited
                   from them custom view class

        :param request: The request sent to the view
        :type var: WSGIRequest

        """
        view.request = request
        view.args = args
        view.kwargs = kwargs
        view.request.session = self.client.session
        return view

    def helper_get_response(self, view_name, product_id, quantity):
        """
        Returns response after posting the product data
        """

        return self.client.post(reverse(view_name), {
            "items": json.dumps([{
                "product_id": product_id,
                "quantity": quantity,
            }])
        })

    def helper_cart_errors(self, product_id, quantity, expected_msg):
        """
        Common code shared by the error checking functions
        """
        view_names = ["add_to_cart", "update_cart"]
        for view_name in view_names:
            response = self.helper_get_response(
                view_name, product_id, quantity)
            self.assertEqual(response.status_code, 200)
            json_response = json.loads(response.content)
            self.assertEqual(json_response["success"], 0)
            self.assertEqual(json_response["err_msg"], expected_msg)

    def test_no_product_error(self):
        """
        Test if the AJAX will return an error
        if is submitted an unexisting
        product id
        """
        self.helper_cart_errors(
            product_id=str(self.product.pk + 1),
            quantity="5",
            expected_msg=settings.ERR_MSG_NO_PRODUCT
        )

    def test_cart_invalid_args(self):
        """
        Test if the AJAX will return error
        if are submitted invalid parameters
        """

        self.helper_cart_errors(
            product_id="5",
            quantity="x",
            expected_msg=settings.ERR_MSG_INVALID_PARAMS
        )
        self.helper_cart_errors(
            product_id="x",
            quantity="5",
            expected_msg=settings.ERR_MSG_INVALID_PARAMS
        )
        self.helper_cart_errors(
            product_id="x",
            quantity="y",
            expected_msg=settings.ERR_MSG_INVALID_PARAMS
        )
        self.helper_cart_errors(
            product_id={},
            quantity=[],
            expected_msg=settings.ERR_MSG_INVALID_PARAMS
        )

    def test_add_to_cart(self):
        """
        Test if a product can be added to cart
        """
        str_product_id = str(self.product.pk)
        response = self.helper_get_response("add_to_cart", str_product_id, "2")
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response["success"], 1)
        self.assertEqual(json_response["items_in_cart"], 1)
        self.assertEqual(json_response["cart"]
                         [str_product_id]["quantity"], "2")
        self.assertEqual(
            float(
                json_response["cart"][str_product_id]["product_data"]["price"]
            ),
            float(self.product.price)
        )
        self.assertEqual(
            json_response["cart"][str_product_id]["product_data"]["id"],
            str_product_id
        )
        self.added_item_id = str_product_id

    def test_update_cart(self):
        """
        Test if a product can be updated in the cart
        """
        if not hasattr(self, 'added_item_id'):
            self.test_add_to_cart()
        str_product_id = self.added_item_id
        response = self.helper_get_response("update_cart", str_product_id, "6")
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response["success"], 1)
        self.assertEqual(json_response["items_in_cart"], 1)
        self.assertEqual(json_response["cart"]
                         [str_product_id]["quantity"], "6")
        self.assertTrue(
            "product_data" in json_response["cart"][str_product_id])

    def test_delete_from_cart(self):
        """
        Test if a product can be updated in the cart
        """
        if not hasattr(self, 'added_item_id'):
            self.test_add_to_cart()
        str_product_id = self.added_item_id
        view_names = ["add_to_cart", "update_cart"]
        for view_name in view_names:
            response = self.helper_get_response(view_name, str_product_id, "0")
            self.assertEqual(response.status_code, 200)
            json_response = json.loads(response.content)
            self.assertEqual(json_response["success"], 1)
            self.assertEqual(json_response["items_in_cart"], 0)
            self.assertFalse(str_product_id in json_response["cart"])

    def test_set_init_vars(self):
        self.view.set_init_vars()
        # Empty cart
        self.assertEqual(self.view.success, 1)
        self.assertEqual(self.view.items_in_cart, 0)
        self.assertEqual(self.view.err_msg, "")
        self.assertEqual(self.view.cart, {})
        # Non empty cart
        self.view.request.session = {"cart": "item"}
        self.view.set_init_vars()
        self.assertEqual(self.view.success, 1)
        self.assertEqual(self.view.items_in_cart, 0)
        self.assertEqual(self.view.err_msg, "")
        self.assertEqual(self.view.cart, "item")

    def test_set_cart(self):
        self.view.request.session["cart"] = "item"
        """ Test if the cart is removed from the session
        if there are no intems inside """
        self.view.items_in_cart = 0
        self.view.set_cart()
        self.assertEqual(self.view.cart, {})
        """ Test if the cart is assigned properly to the cart
        attribute if there are intems inside """
        self.view.request.session["cart"] = "item"
        self.view.items_in_cart = 1
        self.view.set_cart()
        self.assertEqual(self.view.cart, "item")

    def test_return_error(self):
        self.view.items_in_cart = 0
        self.view.cart = {}
        response = (self.view.return_error("Error msg"))
        json_ = json.loads(response.content)
        self.assertEqual(json_["err_msg"], "Error msg")
        self.assertEqual(json_["success"], 0)

    def test_delete_product_from_cart(self):
        product_id = "5"
        self.view.request.session["cart"] = {}
        self.view.request.session["cart"][product_id] = "some product data"
        self.view.delete_product_from_cart(product_id)
        self.assertTrue(product_id not in self.view.request.session["cart"])

    def test_update_cart_with_product(self):
        product_id = str(self.product.pk)
        quantity = "4"
        product = Product.objects.filter(id=product_id)
        self.view.request.session["cart"] = {}
        self.view.update_cart_with_product(product_id, quantity, product)
        self.assertTrue(product_id in self.view.request.session["cart"])
        self.assertIsInstance(
            self.view.request.session["cart"][product_id], dict)
        self.assertEqual(
            self.view.request.session["cart"][product_id]["quantity"],
            quantity
        )
        product_data = {
            k: str(v) for k, v in
            product.values()[0].items()
        }
        self.assertEqual(
            self.view.request.session["cart"][product_id]["product_data"],
            product_data
        )

    def test_return_json(self):
        cart = {"item": "item_data"}
        self.view.success = 1
        self.view.err_msg = ""
        self.view.items_in_cart = "5"
        self.view.cart = cart
        response = (self.view.return_json())
        json_ = json.loads(response.content)
        self.assertEqual(json_["success"], 1)
        self.assertEqual(json_["err_msg"], "")
        self.assertEqual(json_["items_in_cart"], "5")
        self.assertEqual(json_["cart"], cart)

    def test_is_valid_ajax_input(self):
        self.assertEqual(self.view.is_valid_ajax_input(("4", "5")), True)
        self.assertEqual(self.view.is_valid_ajax_input(("4", 5)), False)
        self.assertEqual(self.view.is_valid_ajax_input((4, 5)), False)
        self.assertEqual(self.view.is_valid_ajax_input(([], {})), False)
        self.assertEqual(self.view.is_valid_ajax_input(("b", "a")), False)

    def tearDown(self):
        self.delete_product_image()
