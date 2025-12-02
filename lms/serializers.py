from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile, Course, Lesson, Enrollment,
    Comments
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User model"""
    password = serializers.CharField(
        write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'is_active', 'date_joined', 'password']
        read_only_fields = ['id', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    class Meta:
        model = Profile
        fields = ['id', 'user', 'phone', 'avatar', 'is_instructor', 'is_active','created_at','password']
        read_only_fields = ['id', 'created_at']



class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model"""

    class Meta:
        model = Course
        fields = [
            'id', 'course_name', 'num_lessons'
        ]
        read_only_fields = ['id']


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson model"""

    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'lesson_name', 'category', 'description'
        ]
        read_only_fields = ['id', 'course', 'lesson_name']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model"""

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'status', 'rol_course'
        ]
        read_only_fields = ['id', 'enrolled_at', 'completed_at']


class CommentsSerializer(serializers.ModelSerializer):
    """Serializer for LessonProgress model"""

    class Meta:
        model = Comments
        fields = [
            'course', 'comment'
        ]
        read_only_fields = ['course']


