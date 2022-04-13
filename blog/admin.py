from django.contrib import admin
from calendar import c
import django
from .models import red_flag,Category,UserProfile,invention_records,Location,Contact,Post


# Register your models here.
from .models import Video
admin.site.register(Video)

# Register your models here.

admin.site.register(red_flag)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(invention_records)
admin.site.register(Location)
admin.site.register(Contact)
admin.site.register(Post)
