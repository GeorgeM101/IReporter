from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserProfileForm



# Create your views here.
def profile(request):
	
	# up_form = UserProfileForm(instance=request.user.userprofile)
	# result = "error"
	# message = "Something went wrong. Please check and try again"

	if request.method == "POST":
		up_form = UserProfileForm(data = request.POST, instance=request.user.userprofile)
		
		#if both forms are valid, do something
		if up_form.is_valid():
			user = up_form.save()

			# up = request.user.userprofile
			# up.has_profile = True
			# up.save()

			result = "perfect"
			message = "Your profile has been updated"
			context = {"result": result, "message": message,}
		else:
			context = {"result": result, "message": message}

		return HttpResponse(
			json.dumps(context),
			content_type="application/json"
			)
		
	context = {
		'google_api_key': settings.GOOGLE_API_KEY
		}
	return render(request, 'profile.html', context)
