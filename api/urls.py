# from django.urls import path
# from . import views
#
# app_name = 'api'
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('create/', views.post, name='pass'),
# ]

from django.urls import path
from django.contrib import admin
from .views import shorten_url, redirect_original

urlpatterns = [
    path('', shorten_url, name='shorten_url'),
    path('admin/', admin.site.urls),
    path('<str:short_url>/', redirect_original, name='redirect_original'),
]