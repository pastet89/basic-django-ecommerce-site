from django.test import TestCase
from django.db import models
from django.conf import settings
from .templatetags import add_pk_to_slug
from .models import Category, Product
from .forms import CategoryForm, CheckoutForm
from decimal import Decimal
from mptt.admin import DraggableMPTTAdmin
from django.core.files.uploadedfile import SimpleUploadedFile
from .admin import CategoryDraggableMPTTAdmin, ProductModelAdmin
from django.template.defaultfilters import slugify
from django.contrib import admin
from datetime import datetime
import os
import unittest
# Create your tests here.

"""
##############################
     Template tags tests
#############################
"""


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


"""
##############################
        Admin tests
#############################
"""


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


"""
##############################
        Forms tests
#############################
"""


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


"""
##############################
        Models tests
#############################
"""


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
