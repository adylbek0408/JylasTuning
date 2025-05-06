from django.contrib import admin
from django.urls import path, include
from drf_social_oauth2.views import TokenView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('car_tuning.urls')),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('auth/google/', TokenView.as_view(), name='google-auth'),

]
