from django.db import models
from .City import City

class Location(models.Model):
    name = models.CharField(max_length=100)
    technician_name = models.CharField(max_length=100, default="Unknown Technician")
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
