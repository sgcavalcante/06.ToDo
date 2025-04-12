
import io
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import plotly.express as px
import csv
from django.http import HttpResponse,JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.shortcuts import render,redirect
from .models import TemperaturaSensores,Peso
from .forms import PesoForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from plotly.subplots import make_subplots
#import plotly.graph_objs as go
from django.db.models import Avg, Max, Min, Count

# Create your views here.
def home(request):
    return render(request,'home.html')

def index(request):
    return render(request,'index.html')

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


def sensordata(request):
    sensor_id = request.GET.get('sensor_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    ultimos = request.GET.get('ultimos')

    readings = TemperaturaSensores.objects.all().order_by('-timestamp')
    if start_date:
        readings = readings.filter(timestamp__gte=parse_datetime(start_date))
    if end_date:
        readings = readings.filter(timestamp__lte=parse_datetime(end_date))
    if sensor_id:
        readings = readings.filter(sensor_id=sensor_id)
    if ultimos:
        try:
            qtd = int(ultimos)
            readings = readings[:qtd]
        except ValueError:
            pass

    # Agrupando por sensor para os gráficos
    sensors_data = {}
    local_tz = timezone.get_current_timezone()
    for reading in readings:
        local_timestamp = reading.timestamp.astimezone(local_tz)
        if reading.sensor_id not in sensors_data:
            sensors_data[reading.sensor_id] = {'timestamps': [], 'temperaturas': []}
        sensors_data[reading.sensor_id]['timestamps'].append(local_timestamp)
        sensors_data[reading.sensor_id]['temperaturas'].append(reading.temperatura)

    graphs = []
    for sensor, data in sensors_data.items():
        fig = px.line(
            x=data['timestamps'],
            y=data['temperaturas'],
            title=f'Temperaturas do Sensor {sensor}',
            labels={'x': 'Timestamp', 'y': 'Temperatura (°C)'},
            template='plotly_dark'
        )
        fig.update_traces(mode='markers+lines')
        fig.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, b=0, t=30),
            height=300
        )
        graph_div = fig.to_html(full_html=False)
        graphs.append({'sensor_id': sensor, 'graph_div': graph_div})

    # Resumo por sensor
    resumo = (
        TemperaturaSensores.objects.values('sensor_id')
        .annotate(
            media=Avg('temperatura'),
            max=Max('temperatura'),
            min=Min('temperatura'),
            total=Count('id')
        )
    )

    return render(request, 'sensor_data.html', context={
        'graphs': graphs,
        'readings': readings,
        'resumo': resumo
    })


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
        local_timestamp = data.timestamp1.astimezone(local_tz)
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
        #title_text="Gráficos",
        #width=900,  # defina a largura desejada
        #height=500,
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=30),
        height=450,
        xaxis_title="Timestamp",
        yaxis_title="Peso (kg)"
    )

    #############
    '''
    fig = px.line(
                x=data['timestamps'],
                y=data['temperaturas'],
                title=f'Temperaturas do Sensor {sensor}',
                labels={'x': 'Timestamp', 'y': 'Temperatura (°C)'},
                template='plotly_dark'
            )
            fig.update_traces(mode='markers+lines')
            fig.update_layout(
                autosize=True,
                margin=dict(l=0, r=0, b=0, t=30),
                height=300
            )
    '''
    #############

    # Converter a figura para HTML
    graph_html = pio.to_html(fig, full_html=False)

    #####
    pessoa_data = Peso.objects.order_by('id').last()#(field_name='peso')
     
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = pessoa_data.peso,
    mode = "gauge+number+delta",
    title = {'text': "Peso Atual"},
    delta = {'reference': 95},
    gauge = {'axis': {'range': [None, 120]},
             'steps' : [
                 {'range': [0, 100], 'color': "lightgray"},
                 {'range': [100, 120], 'color': "red"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 95}}))

     
    graph_html1 = pio.to_html(fig, full_html=False)
    #####



    return render(request, 'monitor_peso.html', {'form':form,'graph_html': graph_html,'graph_html1': graph_html1})
    #return render(request,'teste_main.html')

def plot_gauge(request):
    pessoa_data = Peso.objects.order_by('id').last()#(field_name='peso')
    #for data in pessoa_data:
        #print(pessoa_data.peso[0])
    print(pessoa_data.peso)
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = pessoa_data.peso,
    mode = "gauge+number+delta",
    title = {'text': "Speed"},
    delta = {'reference': 95},
    gauge = {'axis': {'range': [None, 200]},
             'steps' : [
                 {'range': [0, 250], 'color': "lightgray"},
                 {'range': [110, 250], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 95}}))

     
    graph_html1 = pio.to_html(fig, full_html=False)
    return render(request, 'plot_gauge.html', {'graph_html1': graph_html1})



def deletar_dados(request):
    dados = TemperaturaSensores.objects.all()
    dados.delete()
    return redirect('sensordata')
   
def deletar_dados_peso(request):
    dados = Peso.objects.all()
    dados.delete()
    return redirect('peso_view')






def grafico_temperatura(request):
    return render(request, 'grafico_temperatura.html')


@api_view(['GET'])
def get_temperatura_data(request):
    limit = request.GET.get('limit')
    
    # Ordena por timestamp descendente (mais recente primeiro)
    sensor_data = TemperaturaSensores.objects.all().order_by('-timestamp')
    
    # Aplica o limite, se informado
    if limit:
        try:
            limit = int(limit)
            sensor_data = sensor_data[:limit]
        except ValueError:
            pass  # Se o valor não for numérico, ignora o filtro

    # Agrupa por sensor_id
    sensors_groups = {}
    local_tz = timezone.get_current_timezone()
    for data in reversed(sensor_data):  # reversed para voltar à ordem cronológica
        local_timestamp = data.timestamp.astimezone(local_tz)
        if data.sensor_id not in sensors_groups:
            sensors_groups[data.sensor_id] = {'timestamps': [], 'temperatures': []}
        sensors_groups[data.sensor_id]['timestamps'].append(local_timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        sensors_groups[data.sensor_id]['temperatures'].append(data.temperatura)

    return JsonResponse(sensors_groups)


def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="leituras.csv"'

    writer = csv.writer(response)
    writer.writerow(['Sensor ID', 'Temperatura (°C)', 'Timestamp'])

    dados = TemperaturaSensores.objects.all().order_by('-timestamp')
    for leitura in dados:
        writer.writerow([leitura.sensor_id, leitura.temperatura, leitura.timestamp])

    return response