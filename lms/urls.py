from django.urls import path, include
from . import views

# App URL patterns (site pages). The API router is mounted at project-level
urlpatterns = [
    path('', views.index, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('cursos/<int:course_id>',views.course_info,name='curso'),
    path('cursos/lesson_test/',views.lesson_test,name='test'),
    path('activate/<int:user_id>/', views.activate_account, name='activate'),
    path('ajax/courses/', views.list_courses_ajax, name='list_courses_ajax'),
    path('ajax/courses/create/', views.inscribir_curso,name='new_course_ajax'),
    path('inscripcion/<int:course_id>',views.inscripcion,name='Inscribir_nuevo_cursos'),
    
]
