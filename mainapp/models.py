from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(max_length=100, primary_key=True, null=False)
    name = models.CharField(max_length=50)
    number_reviews = models.IntegerField()
    password = models.CharField(max_length=400, null=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]

    class Meta:
        managed=False
        db_table='user'