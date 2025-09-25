from django.db import models
from django.contrib.auth.models import User
from api.models.Location import Location

class ECGClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    # Optional: add more fields, like institutions, contact info, etc.

    def __str__(self):
        return self.user.username
