import email
from django.db import models
from accounts.models import User

# Create your models here.
class Cart(models.Model):
    email = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    items = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.email.email