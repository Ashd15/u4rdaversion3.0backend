from django.contrib.auth.models import User
from django.db import models


class InstPersonalInfo(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    instadd = models.CharField(max_length=100)
    cnprname = models.CharField(max_length=230)
    cnprdesignation = models.CharField(max_length=225)
    cnprphone = models.CharField(max_length=210)
    altcnprname = models.CharField(max_length=230)
    altcnprdesignation = models.CharField(max_length=225)
    altcnprphone = models.CharField(max_length=210)
    emailfraccount = models.EmailField(max_length=250)
    accountcnpr = models.CharField(max_length=215)
    acccnprphone = models.CharField(max_length=210)
