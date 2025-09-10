from django.db import models
from django.contrib.auth.models import User
from .Xray_Location import XLocation
class CorporateDoctor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    location = models.ForeignKey(XLocation, on_delete=models.CASCADE, null=True, blank=True)
    institution_name = models.CharField(max_length=250, blank=True, null=True, default="None")