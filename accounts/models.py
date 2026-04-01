from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLES_CHOICES = (
        ('admin','Admin'),
        ('staff','Staff'),
        ('customer','Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLES_CHOICES, default='customer')
    phone = models.CharField(max_length=15,blank=True,null=True)

    def __str__(self):
        return self.username