from django.shortcuts import render,redirect
from rest_framework import viewsets
from .models import Lessons,Comments,Courses,Profile,Inscriptions
from .serializers import ProfileSerializer,LessonsSerializer,CoursesSerialzer, CommentsSerializer, InscriptionsSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.
def index(request):
    return render(request,'indext.html')


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    ordering = ['creation_date']
    search_fields = ['avatar','Region','is_active']



class LessonsViewSet(viewsets.ModelViewSet):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated]

class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_Class = CoursesSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields=['course_name','num_lessons']

    def perform_create(self,serializer):
        serializer.save(instructor=self.request.user)

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscriptions.objects.all()
    serializer_class = InscriptionsSerializer
    permission_classes = [IsAuthenticated]

