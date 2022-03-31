from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserLocation(models.model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(verbose_name='Longitude', max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name='Latitude', max_length=50, null=True, blank=True)