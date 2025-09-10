from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class EcgReport(models.Model):
    pdf_file = models.FileField(upload_to='uploads/ecg_pdfs/', storage=S3Boto3Storage())
    name = models.CharField(max_length=255, blank=True, null=True)
    patient_id = models.CharField(max_length=255, blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)
    report_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=220, blank=True, null=True)

    def get_pdf_url(self):
      return self.pdf_file.url

    def __str__(self):
        return str(self.pdf_file)
