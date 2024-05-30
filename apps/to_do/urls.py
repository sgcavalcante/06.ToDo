# core/urls.py
from django.urls import path
from apps.to_do.views import home

urlpatterns = [
    path('', home, name='home'),
]
