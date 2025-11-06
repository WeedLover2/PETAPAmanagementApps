from .models import IoTDevice, SensorData
from rest_framework import serializers

class IoTDeviceSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = IoTDevice
        fields = ['device_id', 'name', 'last_active', 'is_active', 'status']

class SensorDataSerializer(serializers.ModelSerializer):
    device = IoTDeviceSerializer(read_only=True)

    class Meta:
        model = SensorData
        fields = ['device', 'is_smoke_detected', 'is_vibration_detected', 'timestamp']