from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm
from django.http import JsonResponse
import json

from .models import (
    Profile, Comments, Course, Lesson, Enrollment,
)
from .serializers import (
    UserSerializer, ProfileSerializer, CommentsSerializer, CourseSerializer,
    LessonSerializer, EnrollmentSerializer)



def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            messages.success(
                request, 'Registro exitoso, revisa tu correo para activar.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def iniciar_sesion(request):
    # Detect whether a Google SocialApp is configured for allauth so the
    # template can safely show/hide the provider login link.
    google_provider_enabled = False
    try:
        from allauth.socialaccount.models import SocialApp
        google_provider_enabled = SocialApp.objects.filter(
            provider='google').exists()
    except Exception:
        # allauth may not be available or DB may not have SocialApp entries.
        google_provider_enabled = False

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil')
        else:
            messages.error(request, 'Credenciales incorrectas')
            # Redirect to home so the base template (which contains the login modal)
            # will render the messages and our JS will keep the modal open.
            return redirect('home')
    return render(request, 'usuarios/login.html', {'google_provider_enabled': google_provider_enabled})


@login_required
def perfil(request):
    user = request.user
    enrollments = Enrollment.objects.filter(student = user)
    courses = Course.objects.filter(id__in = enrollments.values_list('course_id', flat=True))
    return render(request, 'usuarios/perfil.html',{'courses':courses})


def cerrar_sesion(request):
    logout(request)
    return redirect('home')

@login_required
def index(request):
    # Show up to 20 published courses on the home page
    courses = Course.objects.all()
    return render(request, 'index.html', {'courses': courses})


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'date_joined']
    ordering = ['username']


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Profile model"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_instructor']
    search_fields = ['user__username']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course model"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['num_lessons']
    search_fields = ['course_name']
    ordering_fields = ['course_name']
    ordering = ['course_name']


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for Lesson model"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course', 'category']
    search_fields = ['lesson_name', 'description']
    ordering_fields = ['lesson_name']
    ordering = ['course']


class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment model"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'course', 'student']
    search_fields = ['course_name']
    ordering_fields = ['status']
    ordering = ['status']

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for LessonProgress model"""
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def perform_create(self, serializer):
        serializer.save(course=self.request.course)


def activate_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    return redirect('login')

@login_required
def list_courses_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        courses = list(Course.objects.all().values(
            'id', 'course_name', 'num_lessons'))
        return JsonResponse({'courses': courses})
    return JsonResponse({'error': 'bad request'}, status=400)

@login_required
def inscribir_curso(request, course_id):
    """Enroll the current user in a course"""
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is already enrolled
    enrollment, deleted = Enrollment.objects.delete()
    
    if deleted:
        messages.success(request, f'Te has desinscrito exitosamente')
    else:
        messages.info(request, f'No estabas asignado al curso')
    
    return redirect('home')

@login_required
def inscripcion(request,course_id):
    course = get_object_or_404(Course,id=course_id)

    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info(request, "Ya estás inscrito en este curso.")
        return redirect('/perfil/')
    Enrollment.objects.create(
        student=request.user,
        course=course,
        status='active',
        rol_course='student'
    )
    messages.success(request, "Te has inscrito en el curso.")
    return redirect('/perfil/')


def course_info(request,course_id):
    lessons = Lesson.objects.filter(course_id=course_id)
    return render(request, 'usuarios/cursos.html', {'lessons':lessons})

def lesson_test(request):
    return render(request, 'usuarios/lesson_view.html')


    
    
    
        