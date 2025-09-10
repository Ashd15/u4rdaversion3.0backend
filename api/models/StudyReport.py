from django.db import models

class StudyReport(models.Model):
    study_id = models.CharField(max_length=255, unique=True)
    editor_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.study_id
