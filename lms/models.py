from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver




class Profile(models.Model):
    """Extended user profile for LMS users"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_instructor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.username})"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Course(models.Model):
    course_name = models.CharField(max_length=50, unique=True, default="")
    num_lessons = models.IntegerField(default=0)

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ['course_name']
        verbose_name = "Course"
        verbose_name_plural = "Courses"

#Hijo de la clase Courses
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_name= models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.course.course_name} - {self.lesson_name}"

    class Meta:
        ordering = ['lesson_name']
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

#Hijo de las clases Profile y courses
class Enrollment(models.Model):
    """Student enrollment in courses (inscriptions)"""
    ENROLLMENT_STATUS = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended'),
    ]

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(
        max_length=20, choices=ENROLLMENT_STATUS, default='active')
    rol_course = models.CharField(max_length=20, default="student")

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.course_name}"

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['status']
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

class Comments(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.CharField()

