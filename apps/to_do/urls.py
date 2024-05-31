# core/urls.py
from django.urls import path
from apps.to_do.views import home,monitortemp,line_chart_view,line_chart_page

urlpatterns = [
    path('', home, name='home'),
    path('monitortemp', monitortemp, name='monitortemp'),
    path('line-chart/', line_chart_view, name='line_chart'),
    path('line-chart-page', line_chart_page, name='line_chart_page'),
]
