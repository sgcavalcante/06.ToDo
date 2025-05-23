# core/urls.py
from django.urls import path,include
from apps.to_do.views import index,home,sensordata,receive_data,plot_view,deletar_dados,peso_view,deletar_dados_peso,get_temperatura_data,grafico_temperatura,plot_gauge,exportar_csv
urlpatterns = [ 
    path('home', home, name='home'),
    path('', index, name='index'),
    
    path('sensordata/',sensordata,name='sensordata'),
    path('api/receive-data/', receive_data, name='receive_data'),
    path('plot/', plot_view, name='plot_view'),
    path('deletar_dados/', deletar_dados, name='deletar_dados'),
    path('peso_view/', peso_view, name='peso_view'),
    path('deletar_dado_peso/', deletar_dados_peso, name='deletar_dados_peso'),
    path('grafico_temperatura/', grafico_temperatura, name='grafico_temperatura'),  # Rota para o template
    path('api/get_temperatura_data/', get_temperatura_data, name='get_temperatura_data'),
    path('plot_gauge', plot_gauge, name='plot_gauge'),
    path('exportar_csv/', exportar_csv, name='exportar_csv'),
    
]
