
import io
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from .models import TemperaturaSensores
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def home(request):
    return render(request,'home.html')

def monitortemp(request):
    return render(request,'MonitorTemp.html')




@api_view(['POST'])
def receive_data(request):
    try:
        sensor_id = request.data.get('sensor_id')
        temperatura = request.data.get('temperatura')
        if sensor_id is not None and temperatura is not None:
            reading = TemperaturaSensores(sensor_id=sensor_id, temperatura=temperatura)
            reading.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Missing id or temperatura'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'failure', 'message': str(e)}, status=500)
    
#def sensor_data(request):
#    readings=TemperaturaSensores.objects.all().order_by('-timestamp')
#    return render(request,'sensor_data.html',{'readings':readings})
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import plotly.express as px
#from django.shortcuts import render
#from .models import TemperaturaSensores

import plotly.express as px
#from django.shortcuts import render
#from .models import TemperaturaSensores
from django.utils.dateparse import parse_datetime

def sensor_data(request):
    # Parâmetros de filtro
    sensor_id = request.GET.get('sensor_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filtrar os dados
    readings = TemperaturaSensores.objects.all().order_by('-timestamp')
    if sensor_id:
        readings = readings.filter(sensor_id=sensor_id)
    #if start_date:
        #readings = readings.filter(timestamp__gte=parse_datetime(start_date))
    #if end_date:
        #readings = readings.filter(timestamp__lte=parse_datetime(end_date))

    # Extrair os dados para o gráfico
    sensor_ids = [reading.sensor_id for reading in readings]
    temperaturas = [reading.temperatura for reading in readings]
    timestamps = [reading.timestamp for reading in readings]

    # Criar o gráfico com Plotly
    fig = px.line(x=timestamps, y=temperaturas, title='Temperaturas dos Sensores', labels={'x': 'Timestamp', 'y': 'Temperature (°C)'})
    fig.update_traces(mode='markers+lines')
    fig.update_layout(autosize=True, margin=dict(l=0, r=0, b=0, t=30))

    # Converter o gráfico para JSON
    graph_json = fig.to_json()

    return render(request, 'sensor_data.html', {'graph_json': graph_json, 'readings': readings})