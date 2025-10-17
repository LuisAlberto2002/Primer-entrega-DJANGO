from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    Region = models.CharField(max_length=15, default='None')
    avatar = models.ImageField(default='')
    phone = models.CharField(max_length=30, default='')
    creation_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=20)

class Courses(models.Model):
    course_name = models.CharField(max_length=50)
    num_lessons = models.IntegerField(default=0)

#Hijo de la clase Courses
class Lessons(models.Model):
    id_course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    lesson_name= models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

#Hijo de las clases User y courses
class Inscriptions(models.Model):
    id_course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    rol_course = models.CharField(max_length=20)
    
#Hijo de la clase Inscriptions
class Comments(models.Model):
    id_courses = models.ForeignKey(Courses, on_delete=models.CASCADE)

    comment = models.CharField()
