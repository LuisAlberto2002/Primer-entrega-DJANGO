from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
#from Project import views as Project_views
#from lms import views as lms_views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Aplicacion elaborada con Django, conectada a una base de datos Postgres" \
      "Aplicaicon de cursos con usuarios multi-rol (Usuarios/Profesores) incluye cursos, incripciones, roles, etc. ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@lms.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Project.urls")),
    path("api/Project/", include("Project.urls")),
    path("api-auth", include("rest_framework.urls")),
    re_path('swagger(?P<format>/.json|/.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]