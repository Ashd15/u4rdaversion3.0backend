from django.contrib.auth.models import User
from django.db import models

class CKEditorTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.name
