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
    
from django.db import models
from datetime import datetime as dt
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at','-created_at']

    def save_category(self):
        self.save()

    def update_category(self,name,description):
        self.name=name
        self.description=description
        self.save()

    def delete_category(self):
        self.delete()

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at','-created_at']

    def save_location(self):
        self.save()

    def update_location(self,name):
        self.name=name
        self.save()

    def delete_location(self):
        self.delete()

    def __str__(self):
        return self.name


class invention_records(models.Model):
    name = models.CharField(max_length=70)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    occupants_count = models.IntegerField(default=0)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at','-created_at']

    def save_invention_records(self):
        self.save()

    def update_invention_records(self,name,location,occupants_count,admin):
        self.name=name
        self.location=location
        self.occupants_count=occupants_count
        self.admin=admin
        self.save()

    def delete_neigborhood(self):
        self.save()

    @classmethod
    def delete_invention_records(cls, id):
        cls.objects.filter(id=id).delete()

    @classmethod
    def update_invention_records(cls, id):
        cls.objects.filter(id=id).update()

    @classmethod
    def search_by_name(cls, search_term):
        hood = cls.objects.filter(name__icontains=search_term)
        return hood


    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    invention_records = models.ForeignKey(invention_records, on_delete=models.CASCADE)
    profile_pic = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at','-created_at']

    def save_userProfile(self):
        self.save()

    def update_userProfile(self,name,email,location,neighbourhood,profile_pic):
        self.name=name
        self.email=email
        self.location=location
        self.neighbourhood=neighbourhood
        self.profile_pic=profile_pic
        self.save()

    def delete_userProfile(self):
        self.delete()

    def __str__(self):
        return self.name


class red_flag(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invention_records = models.ForeignKey(invention_records, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at','-created_at']

    def create_red_flag(self):
        self.save()

    def update_red_flag(self,name,email,description,user,invention_records):
        self.name=name
        self.email=email
        self.description=description
        self.user=user
        self.invention_records=invention_records
        self.save()

    def delete_red_flag(self):
        self.delete()

    @classmethod
    def search_by_name(cls, search_term):
        red_flag = cls.objects.filter(name__icontains=search_term)
        return red_flag


    @classmethod
    def find_red_flag(cls, red_flag_id):
        found_red_flag = cls.objects.get(id=red_flag_id)
        return found_red_flag

    def __str__(self):
        return self.name


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100)
    invention_records = models.ForeignKey(invention_records, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering=['-updated_at','-created_at']

    def save_contact(self):
        self.save()

    def update_contact(self,name,telephone,email,user,neighbourhood):
        self.name=name
        self.email=email
        self.telephone=telephone
        self.user=user
        self.invention_records=invention_records
        self.save()

    def delete_contact(self):
        self.delete()

    @classmethod
    def search_by_name(cls, search_term):
        contact = cls.objects.filter(name__icontains=search_term)
        return contact


    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    invention_records = models.ForeignKey(invention_records, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at','-created_at']

    def save_post(self):
        self.save()

    def update_post(self,category,title,content,image,user,location,neighbourhood):
        self.category=category
        self.title=title
        self.content=content
        self.image=image
        self.user=user
        self.location=location
        self.invention_records=invention_records
        self.save()

    def delete_post(self):
        self.delete()

    @classmethod
    def search_by_title(cls, search_term):
        post = cls.objects.filter(title__icontains=search_term)
        return post


    def __str__(self):
        return self.title

