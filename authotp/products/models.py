from django.db import models

# Create your models here.
class Product(models.Model):
    image = models.ImageField(upload_to='images')
    name = models.CharField(max_length=255, blank=True)
    price = models.IntegerField(blank=True)
    sold = models.IntegerField(blank=True)
    shipping = models.IntegerField(blank=True)

    def __str__(self):
        return self.name