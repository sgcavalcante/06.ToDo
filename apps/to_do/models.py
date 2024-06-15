from django.db import models

# Create your models here.
class TemperaturaSensores(models.Model):
    sensor_id = models.IntegerField(blank=True,null=True)
    temperatura = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sensor {self.sensor_id} - {self.temperatura}°C at {self.timestamp}'
    


class Peso(models.Model):
    pessoa_id = models.IntegerField(blank=True,null=True)
    peso = models.FloatField(blank=False,null=False)
    timestamp1 = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f'Peso: {self.pessoa_id} - {self.peso} kg at {self.timestamp1}'