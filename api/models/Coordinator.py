from django.db import models

class Coordinator(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    about = models.TextField(null=True, blank=True)  # short bio/about section
    profile_pic = models.ImageField(
        upload_to="coordinator_profiles/", null=True, blank=True
    )

    # TAT (Turnaround Time) stats
    tat_completed = models.PositiveIntegerField(default=0)
    tat_breached = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)  # track when added
    updated_at = models.DateTimeField(auto_now=True)      # track last update


    def __str__(self):
        return self.first_name
