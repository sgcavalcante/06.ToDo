from django.db import models

# Create your models here.
class TemperaturaSensores(models.Model):
    sensor_id = models.IntegerField(blank=True,null=True)
    temperatura = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sensor {self.sensor_id} - {self.temperatura}°C at {self.timestamp}'