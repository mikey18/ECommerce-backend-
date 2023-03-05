from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
# from django.utils.translation import gettext_lazy as _
 

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_superuser", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if other_fields.get("is_superuser") is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        # if user_name is None:
        #     raise ValueError('Users must provide a username')
        if email is None:
            raise ValueError('Users must provide an email address')
       

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user
    

class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    username = None

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return self.email

class Token(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    otp = models.CharField(max_length=200)

    def __str__(self):
        return self.email.email



        