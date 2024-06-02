
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


def sensor_data(request):
    readings=TemperaturaSensores.objects.all().order_by('-timestamp')
    return render(request,'sensor_data.html',{'readings':readings})


@api_view(['POST'])
def receive_data(request):
    try:
        id = request.data.get('id')
        temperatura = request.data.get('temperatura')
        if id is not None and temperatura is not None:
            reading = TemperaturaSensores(id=id, temperatura=temperatura)
            reading.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Missing id or temperatura'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'failure', 'message': str(e)}, status=500)