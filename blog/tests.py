from django.test import TestCase
from .models import Post, Category, UserProfile, Location, invention_records, red_flag, Contact
from django.contrib.auth.models import User

# Create your tests here.

class invention_recordsTestClass(TestCase):
    def setUp(self):
        self.location = Location(name='Test Location')
        self.location.save_location()
        self.admin = User.objects.create_superuser(username='developer',password='password')
        self.invention_records = invention_records(name='Test invention_records', location=self.location, occupants_count=100, admin_id=self.admin.id)

    def test_instance(self):
        self.assertTrue(isinstance(self.invention_records, invention_records))

    def test_save_method(self):
        self.invention_records.save_invention_records()
        invention_records = invention_records.objects.all()
        self.assertTrue(len(invention_records) > 0)

    def test_delete_method(self):
        self.invention_records.save_invention_records()
        self.invention_records.delete()
        invention_records = invention_records.objects.all()
        self.assertTrue(len(invention_records) == 0)


class LocationTestClass(TestCase):
    def setUp(self):
        self.location = Location(name='Test Location')

    def test_instance(self):
        self.assertTrue(isinstance(self.location, Location))

    def test_save_method(self):
        self.location.save_location()
        locations = Location.objects.all()
        self.assertTrue(len(locations) > 0)

    def test_delete_method(self):
        self.location.save_location()
        self.location.delete()
        locations = Location.objects.all()
        self.assertTrue(len(locations) == 0)


class CategoryTestClass(TestCase):
    def setUp(self):
        self.category = Category(name='Test Category')

    def test_instance(self):
        self.assertTrue(isinstance(self.category, Category))

    def test_save_method(self):
        self.category.save()
        categories = Category.objects.all()
        self.assertTrue(len(categories) > 0)

    def test_delete_method(self):
        self.category.save()
        self.category.delete()
        categories = Category.objects.all()
        self.assertTrue(len(categories) == 0)




