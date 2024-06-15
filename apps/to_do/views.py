
import io
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
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
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from django.utils.dateparse import parse_datetime


#opcao 01
'''
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

'''
#opcao 002
'''
def sensor_data(request):
    # Parâmetros de filtro
    sensor_id = request.GET.get('sensor_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filtrar os dados
    readings = TemperaturaSensores.objects.all().order_by('-timestamp')
    if sensor_id:
        readings = readings.filter(sensor_id=sensor_id)
    if start_date:
        readings = readings.filter(timestamp__gte=parse_datetime(start_date))
    if end_date:
        readings = readings.filter(timestamp__lte=parse_datetime(end_date))

    # Extrair os dados para o gráfico
    sensor_ids = [reading.sensor_id for reading in readings]
    temperaturas = [reading.temperatura for reading in readings]
    timestamps = [reading.timestamp for reading in readings]

    # Criar o layout dos subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=('Temperaturas dos Sensores', 'Temperaturas Médias por Sensor'))

    # Primeiro gráfico
    fig1 = px.line(x=timestamps, y=temperaturas, labels={'x': 'Timestamp', 'y': 'Temperature (°C)'})
    fig1.update_traces(mode='markers+lines')

    # Adicionar o primeiro gráfico ao layout dos subplots
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)

    # Segundo gráfico (exemplo: temperatura média por sensor)
    avg_temperaturas = {sensor: [] for sensor in set(sensor_ids)}
    for reading in readings:
        avg_temperaturas[reading.sensor_id].append(reading.temperatura)
    
    avg_temp_values = {sensor: sum(temps) / len(temps) for sensor, temps in avg_temperaturas.items()}
    sensors = list(avg_temp_values.keys())
    avg_temps = list(avg_temp_values.values())

    fig2 = px.bar(x=sensors, y=avg_temps, labels={'x': 'Sensor ID', 'y': 'Average Temperature (°C)'})

    # Adicionar o segundo gráfico ao layout dos subplots
    for trace in fig2.data:
        fig.add_trace(trace, row=2, col=1)

    # Ajustar o layout
    fig.update_layout(autosize=True, margin=dict(l=0, r=0, b=0, t=30))

    # Renderizar o gráfico na página HTML
    graph_div = fig.to_html(full_html=False)
    return render(request, 'sensor_data.html', context={'graph_div': graph_div,'readings':readings})
'''

#opcao 003
from django.shortcuts import render
import plotly.express as px
from .models import TemperaturaSensores
from django.utils.dateparse import parse_datetime
from django.utils import timezone

def sensor_data(request):
    # Parâmetros de filtro
    sensor_id = request.GET.get('sensor_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
     
    # Filtrar os dados
    readings = TemperaturaSensores.objects.all().order_by('-timestamp')
    if start_date:
        readings = readings.filter(timestamp__gte=parse_datetime(start_date))
    if end_date:
        readings = readings.filter(timestamp__lte=parse_datetime(end_date))
    if sensor_id:
        readings = readings.filter(sensor_id=sensor_id)

    # Criar um gráfico separado para cada sensor
    sensors_data = {}
    local_tz = timezone.get_current_timezone()
    for reading in readings:
        # Ajustar o timestamp para o fuso horário local
        local_timestamp = reading.timestamp.astimezone(local_tz)
        if reading.sensor_id not in sensors_data:
            sensors_data[reading.sensor_id] = {'timestamps': [], 'temperaturas': []}
        sensors_data[reading.sensor_id]['timestamps'].append(local_timestamp)
        sensors_data[reading.sensor_id]['temperaturas'].append(reading.temperatura)

    graphs = []
    for sensor, data in sensors_data.items():
        fig = px.line(x=data['timestamps'], y=data['temperaturas'], title=f'Temperaturas do Sensor {sensor}', labels={'x': 'Timestamp', 'y': 'Temperature (°C)'})
        fig.update_traces(mode='markers+lines')
        fig.update_layout(autosize=True, margin=dict(l=0, r=0, b=0, t=30), width=800, height=400)
        graph_div = fig.to_html(full_html=False)
        graphs.append({'sensor_id': sensor, 'graph_div': graph_div})

    return render(request, 'sensor_data.html', context={'graphs': graphs, 'readings': readings})


# views.py
from django.shortcuts import render
from .models import TemperaturaSensores
import plotly.graph_objs as go
import plotly.io as pio
from django.utils import timezone

def plot_view(request):
    # Extrair os dados do banco de dados
    sensor_data = TemperaturaSensores.objects.all()

    # Agrupar os dados por sensor_id
    sensor_groups = {}
    local_tz = timezone.get_current_timezone()
    for data in sensor_data:
        # Ajustar o timestamp para o fuso horário local
        local_timestamp = data.timestamp.astimezone(local_tz)
        if data.sensor_id not in sensor_groups:
            sensor_groups[data.sensor_id] = {'x': [], 'y': []}
        sensor_groups[data.sensor_id]['x'].append(local_timestamp)
        sensor_groups[data.sensor_id]['y'].append(data.temperatura)

    # Criar a figura
    fig = go.Figure()

    # Adicionar um gráfico para cada sensor_id
    for sensor_id, data in sensor_groups.items():
        fig.add_trace(go.Scatter(
            x=data['x'],
            y=data['y'],
            mode='lines+markers',
            name=f'Sensor {sensor_id}'
        ))

    # Atualizar o layout
    fig.update_layout(
        title_text="Gráficos de Temperatura dos Sensores",
        height=600,
        width=800,
        xaxis_title="Timestamp",
        yaxis_title="Temperatura (°C)"
    )

    # Converter a figura para HTML
    graph_html = pio.to_html(fig, full_html=False)

    return render(request, 'plot.html', {'graph_html': graph_html})


from django.shortcuts import render
from .models import TemperaturaSensores,Peso
from .forms import PesoForm
import plotly.graph_objs as go
import plotly.io as pio
from django.utils import timezone


    # Extrair os dados do banco de dados
def peso_view(request):

    if request.method == 'POST':
        form = PesoForm(request.POST)
        if form.is_valid():
            pessoa_id = form.cleaned_data['pessoa_id']
            peso = form.cleaned_data['peso']
            reading = Peso(pessoa_id=pessoa_id, peso=peso)
            reading.save()
            return redirect('peso_view')  # Redireciona para limpar o formulário
    else:
        form = PesoForm()
    pessoa_data = Peso.objects.all()

    # Agrupar os dados por sensor_id
    pessoas_groups = {}
    local_tz = timezone.get_current_timezone()
    for data in pessoa_data:
        # Ajustar o timestamp para o fuso horário local
        local_timestamp = data.timestamp.astimezone(local_tz)
        if data.pessoa_id not in pessoas_groups:
            pessoas_groups[data.pessoa_id] = {'x': [], 'y': []}
        pessoas_groups[data.pessoa_id]['x'].append(local_timestamp)
        pessoas_groups[data.pessoa_id]['y'].append(data.peso)

    # Criar a figura
    fig = go.Figure()

    # Adicionar um gráfico para cada sensor_id
    for pessoa_id, data in pessoas_groups.items():
        fig.add_trace(go.Scatter(
            x=data['x'],
            y=data['y'],
            mode='lines+markers',
            name=f'Sensor {pessoa_id}'
        ))

    # Atualizar o layout
    fig.update_layout(
        title_text="Gráficos",
        height=600,
        width=800,
        xaxis_title="Timestamp",
        yaxis_title="Peso (kg)"
    )

    # Converter a figura para HTML
    graph_html = pio.to_html(fig, full_html=False)

    return render(request, 'monitor_peso.html', {'form':form,'graph_html': graph_html})
   


def deletar_dados(request):
    dados = TemperaturaSensores.objects.all()
    dados.delete()
    return render(request, 'sensor_data.html')
   
def deletar_dados_peso(request):
    dados = Peso.objects.all()
    dados.delete()
    return render(request, 'monitor_peso.html')