from django.contrib import admin

# Register your models here.
from .models import Profile, Courses,Comments,Lessons, Inscriptions

admin.site.register(Profile)
admin.site.register(Courses)
admin.site.register(Comments)
admin.site.register(Lessons)
admin.site.register(Inscriptions)

# Register your models here.
