from django.test import TestCase
from django.conf import settings
from .templatetags import add_pk_to_slug
from .models import Category, Product
from decimal import Decimal
from mptt.admin import DraggableMPTTAdmin
from django.core.files.uploadedfile import SimpleUploadedFile
from .admin import CategoryDraggableMPTTAdmin, ProductModelAdmin
from django.contrib import admin
import os
import unittest
# Create your tests here.


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
        expected_res = self.category_nodes[0].slug.replace(settings.PK_PLACEHOLDER, str(self.category_nodes[0].pk))
        self.assertEqual(expected_res, func_res)

class AdminTestCase(TestCase):
    
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
            name = "name",
            parent = cls.cat_leaf_node,
            slug = "slug_name"
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
    
    def test_category_model_admin(self):
        """
        Tests if the ModelAdmin uses the draggable Django-MPTT widget.
        """
        self.assertIn(DraggableMPTTAdmin, CategoryDraggableMPTTAdmin.__bases__)

    def test_model_admin_exclude_fields(self):
        """
        Tests if the ModelAdmin excludes the slig field which should be
        auto-generated.
        """
        model_admin_obj = ProductModelAdmin(model=Product, admin_site=admin.AdminSite())
        self.assertIn("slug", model_admin_obj.exclude)
        self.assertEqual(1, len(model_admin_obj.exclude))
    
    def test_limit_categories(self):
        """
        Tests if the ModelAdmin filters the categories in the dropdown
        so products can be added only to leaf nodes.
        """
        model_admin_obj = ProductModelAdmin(model=Product, admin_site=admin.AdminSite())
        category_field = model_admin_obj.formfield_for_foreignkey(Product.category.field, None)
        self.assertEqual(1, len(category_field.queryset.values_list()))
    
    @classmethod
    def tearDownClass(cls):
        """
        Deletes the uploaded test image
        """
        cls.product.image.delete()
