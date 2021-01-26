from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)   # One customer is one user
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=250, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
