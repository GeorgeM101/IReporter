from .models import Video
from django import forms
from django.forms import ModelForm
from .models import Post,Business,Contact


class ProjectUploadForm(ModelForm):
    class Meta:
        model = Post
        fields =['']


class Video_form(forms.ModelForm):
    class Meta:
        model = Video
        fields = ("caption", "video", "description")
