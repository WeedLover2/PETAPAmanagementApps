from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class IoTDevice(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    @property
    def is_online(self):
        threshold = timezone.now() - timedelta(minutes=5)
        return self.last_active >= threshold 
    
    @property
    def status(self):
        return "Online" if self.is_online else "Offline"
    
    class Meta:
        ordering = ['-last_active']


class SensorData(models.Model):
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE)
    is_smoke_detected = models.BooleanField(default=False)
    is_vibration_detected = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

