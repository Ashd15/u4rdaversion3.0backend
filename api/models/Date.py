from django.db import models
from .Location import Location

class Date(models.Model):
    date_field = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date_field)


