from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify
from django.conf import settings
import uuid
import os
# Create your models here.


class Product(models.Model):
    def save_file_with_id_name(self, filename):
        """
        Changes the file name to a random generated uuid
        :param filename: the submitted by default image name
        :type filename: str
        """
        file_ = filename.split(os.sep)[-1]
        extension = ".".join(file_.split(".")[-1:])
        filename = str(uuid.uuid4()) + "." + extension
        return filename

    name = models.CharField(max_length=100)
    category = TreeForeignKey(
        'Category',
        db_index=True,
        on_delete=models.CASCADE
    )
    description = models.TextField(blank=False, max_length=500)
    price = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=save_file_with_id_name)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.CASCADE
    )
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Auto-generates a slug, containing a defined in the settings
        placeholder for the category id, which will be later replaced
        in the templates. The category id can not be included in the
        slug by the time of the creation as the category and its id
        still does not exist.
        """
        self.slug = "/".join([
            slugify(__class__.__name__.lower()),
            settings.PK_PLACEHOLDER,
            slugify(self.name)
        ])
        super(__class__, self).save(*args, **kwargs)
