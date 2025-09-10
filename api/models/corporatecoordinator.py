from django.db import models
from django.contrib.auth.models import User
from .personalinfo import PersonalInfo
class CorporateCoordinator(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    radiologist = models.ManyToManyField(PersonalInfo, blank=True)


    def __str__(self):
        return str(self.user)    