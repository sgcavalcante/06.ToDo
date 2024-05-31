import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Create your views here.
def home(request):
    return render(request,'home.html')

def monitortemp(request):
    return render(request,'MonitorTemp.html')


def plot_to_image():
    # Dados de exemplo
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]
    
    # Cria a figura
    fig, ax = plt.subplots()
    ax.plot(x, y)
    
    # Salva o gráfico em um buffer de bytes
    buffer = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)
    
    # Fecha a figura
    plt.close(fig)
    
    # Retorna o buffer de bytes
    return buffer.getvalue()


def line_chart_view(request):
    image_data = plot_to_image()
    return HttpResponse(image_data, content_type='image/png')

def line_chart_page(request):
    return render(request, 'MonitorTemp.html')