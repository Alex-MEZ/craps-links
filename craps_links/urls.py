from api import services
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('api.urls')),  # Linking the app's URLs,
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('<str:short_url>', services.redirection),
]
