from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from flags.models import UserProfile


class UserProfileForm(forms.ModelForm):

	telephone = forms.CharField(max_length=15, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Telephone..'}))
	address = forms.CharField(max_length=100, required=True,)
	town = forms.CharField(max_length=100, required=True,)
	county = forms.CharField(max_length=100, required=True,)
	post_code = forms.CharField(max_length=8, required=True,)
	country = forms.CharField(max_length=40, required=True,)
	longitude = forms.CharField(max_length=50, required=True,)
	latitude = forms.CharField(max_length=50, required=True,)


	class Meta:
		model = UserProfile
		fields = ('telephone', 'address', 'town', 'county', 'post_code', 'country', 'longitude', 'latitude')

