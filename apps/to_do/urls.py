# core/urls.py
from django.urls import path,include
from apps.to_do.views import home,monitortemp,sensor_data

urlpatterns = [ 
    path('', home, name='home'),
    path('monitortemp', monitortemp, name='monitortemp'),
    path('sensor_data/',sensor_data,name='sensor_data'),
    
]
