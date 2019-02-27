from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import reverse
from django.db import models
from django.conf import settings
from .templatetags import add_pk_to_slug
from .models import Category, Product
from . import views
from .forms import CategoryForm, CheckoutForm
from decimal import Decimal
from mptt.admin import DraggableMPTTAdmin
from django.core.files.uploadedfile import SimpleUploadedFile
from .admin import CategoryDraggableMPTTAdmin, ProductModelAdmin
from django.template.defaultfilters import slugify
from django.contrib import admin
from datetime import datetime
import os
import json
import unittest
# Create your tests here.


class TestingHelper:
    def create_cat_and_product(self):
        test_image_src = settings.MEDIA_ROOT + os.sep + "test-img.png"
        if not os.path.isfile(test_image_src):
            raise unittest.SkipTest("Test image for upload missing!")
        self.cat = Category.objects.create(name="test-cat")
        test_image_upload = SimpleUploadedFile(
            name=test_image_src,
            content=open(test_image_src, 'rb').read(),
            content_type='image/png'
        )
        self.product = Product.objects.create(
            category_id=self.cat.pk,
            name="name",
            description="description",
            price=Decimal(10.00),
            image=test_image_upload,
        )
    
    def delete_product_image(self):
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


class ProductModelAdminTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Creates one Product and two Category objects - on of the categories
        can have products (is leaf node) and the other can't.
        """
        test_image_src = settings.MEDIA_ROOT + os.sep + "test-img.png"
        if not os.path.isfile(test_image_src):
            raise unittest.SkipTest("Test image for upload missing!")
        cls.cat_leaf_node = Category.objects.create()
        cls.cat_no_leaf_node = Category.objects.create(
            name="name",
            parent=cls.cat_leaf_node,
            slug="slug_name"
        )
        cls.test_image_upload = SimpleUploadedFile(
            name=test_image_src,
            content=open(test_image_src, 'rb').read(),
            content_type='image/png'
        )
        cls.product = Product.objects.create(
            category_id=cls.cat_leaf_node.pk,
            name="name",
            description="description",
            price=Decimal(10.00),
            image=cls.test_image_upload,
        )

    def test_model_admin_exclude_fields(self):
        """
        Tests if the ModelAdmin excludes the slig field which should be
        auto-generated.
        """
        model_admin_obj = ProductModelAdmin(
            model=Product,
            admin_site=admin.AdminSite()
        )
        self.assertTrue(hasattr(model_admin_obj, "exclude"))
        self.assertEqual(list(model_admin_obj.exclude), ["slug"])

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

    @classmethod
    def tearDownClass(cls):
        """
        Deletes the uploaded test image
        """
        cls.product.image.delete()



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


class ProductTestCase(TestCase):
    def test_string_representation(self):
        product = Product(name="Milk")
        self.assertEqual(str(product), product.name)

    def test_model_save_fields(self):
        """
        Tests the model fields after model saving
        and tests if the image is uploaded.
        """
        test_image_src = settings.MEDIA_ROOT + os.sep + "test-img.png"
        if not os.path.isfile(test_image_src):
            raise unittest.SkipTest("Test image for upload missing!")
        test_image_upload = SimpleUploadedFile(
            name=test_image_src,
            content=open(test_image_src, 'rb').read(),
            content_type='image/png'
        )
        product = Product(**{
            "name": "Honey",
            "category":  Category.objects.create(),
            "description": "Honey is good",
            "price": Decimal(1.22),
            "image": test_image_upload,
        })
        product.save()
        uploaded_img = settings.MEDIA_ROOT + os.sep + str(product.image)

        self.assertEqual(product.name, "Honey")
        self.assertIsInstance(product.name, str)
        self.assertIsInstance(product.category, Category)
        self.assertEqual(product.description, "Honey is good")
        self.assertIsInstance(product.description, str)
        self.assertIsInstance(product.price, Decimal)
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

        """
        self.client = Client()
        # Test my_view() as if it were deployed at /customer/details
        response = my_view(request)
        #setup_test_environment()
        self.assertEqual(response.status_code, 200)"""

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
        self.assertEqual(common_data["categories"].values()[0]["id"], self.cat.pk)
        
        
    def test_common_data_empty_cart(self):
        """
        Test if common_data() returns proper data when there
        are no items in the cart stored in the session.
        """
        common_data = views.GeneralContextMixin.common_data(self.request)
        self.assertIsInstance(common_data, dict)
        self.assertEqual(common_data["items_in_cart"], 0)
        
    def test_common_data_full_cart(self):
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
        self.assertEqual(common_data["cart"], [self.request.session["cart"]["5"]])
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
        common_data = views.GeneralContextMixin.common_data(self.request, my_dict)
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
        
    def test_cart_view_full_cart(self):
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

    def test_checkout_view_full_cart_valid_referrer(self):
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
        
class CategoryViewTestCase(TestCase):
    def setUp(self):
        test_image_src = settings.MEDIA_ROOT + os.sep + "test-img.png"
        if not os.path.isfile(test_image_src):
            raise unittest.SkipTest("Test image for upload missing!")
        self.client = Client()
        self.factory = RequestFactory()
        self.cat = Category.objects.create(name="test-cat")
        test_image_upload = SimpleUploadedFile(
            name=test_image_src,
            content=open(test_image_src, 'rb').read(),
            content_type='image/png'
        )
        self.product = Product.objects.create(
            category_id=self.cat.pk,
            name="name",
            description="description",
            price=Decimal(10.00),
            image=test_image_upload,
        )

        self.view_url = "/" + self.cat.slug.replace(settings.PK_PLACEHOLDER, str(self.cat.pk)) + "/"
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
        self.assertEqual(response.context["categories"].values()[0]["id"], self.cat.pk)
        self.assertEqual(response.context["products"].values()[0]["id"], self.product.pk)
        
    def tearDown(self):
        self.product.image.delete()

class AJAXSessionCartTestCase(TestCase, TestingHelper):
    
    def setUp(self):
        self.create_cat_and_product()
        self.client = Client()
        self.factory = RequestFactory()
   
    """
        
        def test_output(self):
           response = self.client.post(reverse("add_to_cart"), {
                "items": json.dumps([{
                    "product_id": "x",
                    "quantity": "5",
                }])
           })
           print(response.content)
    """

    


    def test_ajax_session_cart_no_product_error(self):
        self.helper_ajax_session_cart_errors(
            product_id=str(self.product.pk + 1),
            quantity="5",
            expected_msg=settings.ERR_MSG_NO_PRODUCT
        )

    def test_ajax_session_cart_invalid_args(self):
        self.helper_ajax_session_cart_errors(
            product_id="5",
            quantity="b",
            expected_msg=settings.ERR_MSG_INVALID_PARAMS
        )
        self.helper_ajax_session_cart_errors(
            product_id="x",
            quantity="5",
            expected_msg=settings.ERR_MSG_INVALID_PARAMS
        )
        self.helper_ajax_session_cart_errors(
            product_id="x",
            quantity="y",
            expected_msg=settings.ERR_MSG_INVALID_PARAMS
        )
        self.helper_ajax_session_cart_errors(
            product_id={},
            quantity=[],
            expected_msg=settings.ERR_MSG_INVALID_PARAMS
        )

    def helper_ajax_session_cart_errors(self, product_id, quantity, expected_msg):
        response = self.client.post(reverse("add_to_cart"), {
            "items": json.dumps([{
                "product_id": product_id,
                "quantity": quantity,
            }])
        })
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual((json_response["success"]), 0)
        self.assertEqual((json_response["err_msg"]), expected_msg)
    
        
    def tearDown(self):
        self.delete_product_image()
