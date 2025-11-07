from django.shortcuts import render
from rest_framework import viewsets, status
from .models import IoTDevice, SensorData
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import IoTDeviceSerializer, SensorDataSerializer
from django.utils import timezone
# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def iot_data_get(request):
    devices = IoTDevice.objects.all()
    serializer = IoTDeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def iot_data_post(request):

    device_id = request.data.get('device_id')
    serializer = SensorDataSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    device, created = IoTDevice.objects.get_or_create(
        device_id=device_id,
        defaults={'name': f'Device {device_id}'}
    )

    device.save()

    SensorData.objects.create(
        device=device,
        is_smoke_detected=request.data.get('is_smoke_detected', False),
        is_vibration_detected=request.data.get('is_vibration_detected', False)
    )

    return Response({
        'status': 'success',
        'device_id': device.device_id,
        'is_smoke_detected': request.data.get('is_smoke_detected', False),
        'is_vibration_detected': request.data.get('is_vibration_detected', False)
    })
@api_view(['GET'])
@permission_classes([AllowAny])
def summary(request):
    devices = IoTDevice.objects.all()
    online_count = sum(1 for device in devices if device.is_online)
    offline_count = devices.count() - online_count
    serializer = IoTDeviceSerializer(devices, many=True)
    
    return Response({
        'total_devices': len(devices),
        'online_devices': online_count,
        'offline_devices': offline_count
    })


