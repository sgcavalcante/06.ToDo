from django.db import models

# Create your models here.
class TemperaturaSensores(models.Model):
    sensorId = models.IntegerField
    temperatura = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sensor {self.sensor_id} - {self.temperature}°C at {self.timestamp}'