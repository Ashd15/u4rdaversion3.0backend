from django.db import models

class Coordinator(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    # @staticmethod
    # def get_coordinator_first_name(email):
    #     coordinator = Coordinator.objects.filter(email=email).first()
    #     if coordinator:
    #         return coordinator.first_name
    #     return None



    def __str__(self):
        return self.first_name
