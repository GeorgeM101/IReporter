from django.db import models
from django.db import models
from .validators import file_size
from django import forms

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # image = models.ImageField(upload_to='media/profile_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})


# Create your models here.
class Video(models.Model):
    caption = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(
        upload_to="media/profile_pics", validators=[file_size])

    def __str__(self):
        return self.caption
# pip install folium
