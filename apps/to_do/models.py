from django.db import models

# Create your models here.
class TemperaturaSensores(models.Model):
    id = models.IntegerField(primary_key=True)
    temperatura = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sensor {self.id} - {self.temperatura}°C at {self.timestamp}'