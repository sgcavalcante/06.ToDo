# core/urls.py
from django.urls import path,include
from apps.to_do.views import home,monitortemp,sensordata,receive_data,plot_view,deletar_dados,peso_view,deletar_dados_peso
urlpatterns = [ 
    path('', home, name='home'),
    path('monitortemp', monitortemp, name='monitortemp'),
    path('sensordata/',sensordata,name='sensordata'),
    path('api/receive-data/', receive_data, name='receive_data'),
    path('plot/', plot_view, name='plot_view'),
    path('deletar_dados/', deletar_dados, name='deletar_dados'),
    path('peso/', peso_view, name='peso_view'),
    path('deletar_dado_peso/', deletar_dados_peso, name='deletar_dados_peso'),
]
