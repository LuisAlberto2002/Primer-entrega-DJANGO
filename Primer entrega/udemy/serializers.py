from rest_framework import serializers
from .models import Profile,Courses,Inscriptions,Comments,Lessons

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields= ['id','email','username']
        read_only_fields = ['id','email']

class CoursesSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['id','course_name','num_lessons']
        read_only_fields = ['id','course_name','num_lessons']

class InscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Inscriptions
        fields=['id','rol_course']
        read_only_fields = ['id','rol_course']

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields =['id','comment']
        read_only_fields = ['id','comment']

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields =['id','lesson_name','category','description']
        read_only_fields = ['id','lesson_name',]          