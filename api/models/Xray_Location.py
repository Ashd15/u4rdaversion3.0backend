from django.db import models
from .Xray_City import XCity

class XLocation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.ForeignKey(XCity, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
