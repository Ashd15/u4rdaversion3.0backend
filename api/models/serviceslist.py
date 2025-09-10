from django.contrib.auth.models import User
from django.db import models


class ServicesList(models.Model):
    title = models.CharField('title', max_length=255)

    def __str__(self):
        return (self.title)
    
    
