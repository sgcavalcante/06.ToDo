# core/urls.py
from django.urls import path,include
from apps.to_do.views import home,monitortemp

urlpatterns = [
    path('', home, name='home'),
    path('monitortemp', monitortemp, name='monitortemp'),
    
]
