from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
import pytz
from django.utils.timezone import now

class XrayReport(models.Model):
    pdf_file = models.FileField(upload_to='uploads/xray_pdfs/', storage=S3Boto3Storage())
    name = models.CharField(max_length=255, blank=True, null=True)
    patient_id = models.CharField(max_length=255, blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)
    report_date = models.DateField(blank=True, null=True)
    pdf_on_db = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    accession_number = models.CharField(max_length=255, blank=True, null=True)
    institution_name = models.CharField(max_length=250, blank=True, null=True, default="None")

    def save(self, *args, **kwargs):
        if not self.pdf_on_db:  # Set the timestamp only if it isn't already set
            india_tz = pytz.timezone("Asia/Kolkata")
            self.pdf_on_db = now().astimezone(india_tz)
        super(XrayReport, self).save(*args, **kwargs)

    def get_pdf_url(self):
      return self.pdf_file.url

    def __str__(self):
        return str(self.pdf_file)
