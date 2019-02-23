from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify
from .apps import EbagConfig
from django.conf import settings
import uuid
# Create your models here.
# Продукти - имат име, описание, цена снимка.


        
class Product(models.Model):
    def save_file_with_id_name(self, filename):
        img_folder = 'product_img'
        extension = filename.split(".")[-1]
        return '/'.join([EbagConfig.name, settings.STATIC_URL, img_folder, str(uuid.uuid4()) +"."+extension])
        
    name = models.CharField(max_length=100)
    category = TreeForeignKey('Category', null=True, blank=True, db_index=True, on_delete=models.CASCADE)
    description = models.TextField(blank=False, max_length=500)
    price = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    slug = models.SlugField()
    image = models.ImageField(upload_to=save_file_with_id_name)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    class Meta:
        #fix a typo in the admin plural: "Categorys"
        unique_together = (('parent', 'slug',))
        verbose_name_plural = "Categories"
        
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True,  related_name='children', db_index=True, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)

    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = "/".join([
            slugify(__class__.__name__.lower()),
            settings.PK_PLACEHOLDER,
            slugify(self.name)
        ])
        super(__class__, self).save(*args, **kwargs)
    

        
    '''def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
        slugs = [
            __class__.__name__.lower(),
            self.id,
        ]
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs'''
