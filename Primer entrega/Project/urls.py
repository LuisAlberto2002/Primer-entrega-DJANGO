from django.urls import path, include
from rest_framework.routers import DefaultRouter
from udemy import views
from django.contrib import admin



router = DefaultRouter()
router.register(r'profiles',views.ProfileViewSet)
router.register(r'courses',views.CoursesViewSet)
router.register(r'lessons',views.LessonsViewSet)
router.register(r'comments',views.CommentsViewSet)
urlpatterns = [
    path('',include(router.urls)),
    path('admin/', admin.site.urls),



]
