from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    address = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Profile " + str(self.id)
