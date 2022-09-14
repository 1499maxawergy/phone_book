from django.db import models

# Create your models here.

class PhoneBook(models.Model):
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    title = models.CharField(max_length=60)

