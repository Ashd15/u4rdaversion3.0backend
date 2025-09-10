from django.db import models
from .Xray_Client import XClient
from django.contrib.auth.models import User

class XCity(models.Model):
    name = models.CharField(max_length=100)
    client = models.ForeignKey(XClient, on_delete=models.CASCADE)

    def __str__(self):
        return self.name