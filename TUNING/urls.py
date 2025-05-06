from django.contrib import admin
from django.urls import path, include
from drf_social_oauth2.views import TokenView

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Jylas Tuning API",
        default_version='v1',
        description="Документация по API для проекта Jylas Tuning",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@jylastuning.example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('car_tuning.urls')),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('auth/google/', TokenView.as_view(), name='google-auth'),

    # Swagger UI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
