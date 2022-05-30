from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, null=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.task

