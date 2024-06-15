# core/urls.py
from django.urls import path,include
from apps.to_do.views import home,monitortemp,sensor_data,receive_data,plot_view,deletar_dados,peso_view 
urlpatterns = [ 
    path('', home, name='home'),
    path('monitortemp', monitortemp, name='monitortemp'),
    path('sensor-data/',sensor_data,name='sensor_data'),
    path('api/receive-data/', receive_data, name='receive_data'),
    path('plot/', plot_view, name='plot_view'),
    path('deletar_dados/', deletar_dados, name='deletar_dados'),
    path('peso/', peso_view, name='pesdo_view'),
]
