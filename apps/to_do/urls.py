# core/urls.py
from django.urls import path,include
from apps.to_do.views import home,monitortemp,sensor_data,receive_data

urlpatterns = [ 
    path('', home, name='home'),
    path('monitortemp', monitortemp, name='monitortemp'),
    path('sensor-data/',sensor_data,name='sensor_data'),
    path('api/receive-data/', receive_data, name='receive_data'),
]
