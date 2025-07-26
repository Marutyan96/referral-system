from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Referral API",
      default_version='v1',
      description="Документация по API для реферальной системы",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('referral.urls')),  # Все веб-роуты приложения
    path('admin/', admin.site.urls),
    path('api-docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]