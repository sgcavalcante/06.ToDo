
import io
from django.http import HttpResponse
from django.shortcuts import render
from .models import TemperaturaSensores

# Create your views here.
def home(request):
    return render(request,'home.html')

def monitortemp(request):
    return render(request,'MonitorTemp.html')


def sensor_data(request):
    readings=TemperaturaSensores.objects.all().order_by('-timestamp')
    return render(request,'sensor_data.html',{'readings':readings})