from django.db import models


class MetaPixel(models.Model):
    pixel_id = models.CharField(max_length=255, verbose_name="Meta Pixel ID")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated date")
