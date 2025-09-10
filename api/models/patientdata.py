from django.db import models


class PatientInfo(models.Model):
    PatientId = models.CharField(max_length=250)
    PatientName = models.CharField(max_length=270)
    age = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    TestDate = models.CharField(max_length=250, null=True, blank=True)
    ReportDate = models.CharField(max_length=250, null=True, blank=True)
    FarVisionRight = models.CharField(max_length=250, null=True, default=None, blank=True)
    FarVisionLeft = models.CharField(max_length=250, null=True, default=None, blank=True)
    NearVisionRight = models.CharField(max_length=250, null=True, default=None, blank=True)
    NearVisionLeft = models.CharField(max_length=250, null=True, default=None, blank=True)
    ColorBlindness = models.CharField(max_length=250, null=True, default=None, blank=True)
    SphericalRight = models.CharField(max_length=250, null=True, default=None, blank=True)
    CylindricalRight = models.CharField(max_length=250, null=True, default=None, blank=True)
    AxisRight = models.CharField(max_length=250, null=True, default=None, blank=True)
    AddRight = models.CharField(max_length=250, null=True, default=None, blank=True)
    SphericalLeft = models.CharField(max_length=250, null=True, default=None, blank=True)
    CylindricalLeft = models.CharField(max_length=250, null=True, default=None, blank=True)
    AxisLeft = models.CharField(max_length=250, null=True, default=None, blank=True)
    AddLeft = models.CharField(max_length=250, null=True, default=None, blank=True)

    def __str__(self):
        return self.PatientName
