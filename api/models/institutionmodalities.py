from django.db import models


class InstitutionModalities(models.Model):
    mriopt1 = models.CharField(max_length=100)
    mriothers1 = models.CharField(max_length=100)
    ctopt1 = models.CharField(max_length=100)
    ctothers1 = models.CharField(max_length=100)
    xray1 = models.BooleanField()
    others1 = models.BooleanField()
    rdoprefrence = models.CharField(max_length=15)
    exnocase = models.IntegerField()
    urgent = models.CharField(max_length=30)
    nonurgent = models.CharField(max_length=30)
