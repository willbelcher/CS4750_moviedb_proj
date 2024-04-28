from django.db import models
from django.contrib.auth.models import User


class SiteAdmin(models.Model):
    user = models.ForeignKey(User, related_name='siteadmin', on_delete=models.CASCADE)
