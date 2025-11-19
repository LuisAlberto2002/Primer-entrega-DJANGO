from django.contrib import admin

# Register your models here.
from .models import Profile, Comments, Course, Lesson, Enrollment

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Comments)

