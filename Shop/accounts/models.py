from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Customer(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    surname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=20)
    address = models.TextField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'surname', 'phoneNumber', 'address']

    def __str__(self):
        return self.username
