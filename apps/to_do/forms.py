# forms.py
from django import forms

class PesoForm(forms.Form):
    #pessoa_id = forms.CharField(label='pessoa ID', max_length=100)
    peso = forms.FloatField(label='peso(kg)')
