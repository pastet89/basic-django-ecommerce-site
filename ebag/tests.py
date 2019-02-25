from django.test import TestCase
from django.conf import settings
from templatetags import (add_pk_to_slug, 
                               product_img_path)
# Create your tests here.
import unittest


class TestTemplateTags(TestCase):
    def setUp(self):
        pass
        
    def test_product_img_path(self):
        img_str = "start" + settings.STATIC_URL + "end"
        self.assertEqual(product_img_path(img_str), "end")

if __name__ == '__main__':
    unittest.main()
