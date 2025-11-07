from django.shortcuts import render
from rest_framework import status
from .models import IoTDevice, SensorData
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import IoTDeviceSerializer
from django.db.models import Max
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
    """Accepts a POST with device_id and detector states and records a SensorData entry.

    Expected JSON fields:
    - device_id (str) required
    - is_smoke_detected (bool or str) optional, defaults to False
    - is_vibration_detected (bool or str) optional, defaults to False

    The view coerces common string truthy values ("true", "1", "yes", "on") to True.
    """

    def _coerce_bool(value):
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return bool(value)
        val = str(value).strip().lower()
        return val in ("true", "1", "yes", "y", "on")

    device_id = request.data.get('device_id')
    if not device_id:
        return Response({'error': 'device_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    is_smoke = _coerce_bool(request.data.get('is_smoke_detected', False))
    is_vibration = _coerce_bool(request.data.get('is_vibration_detected', False))

    # Get or create device. If it already exists, save() to update auto_now fields (last_active)
    device, created = IoTDevice.objects.get_or_create(
        device_id=device_id,
        defaults={'name': f'Device {device_id}'}
    )
    # touch/save device to update last_active timestamp
    device.save()

    sensor = SensorData.objects.create(
        device=device,
        is_smoke_detected=is_smoke,
        is_vibration_detected=is_vibration
    )

    return Response({
        'status': 'success',
        'device_id': device.device_id,
        'sensor_id': sensor.id,
        'is_smoke_detected': is_smoke,
        'is_vibration_detected': is_vibration
    }, status=status.HTTP_201_CREATED)
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


def home(request):
    total_IOTDevice = IoTDevice.objects.all().count()
    total_online_devices = sum(1 for device in IoTDevice.objects.all() if device.is_online)
    total_offline_devices = total_IOTDevice - total_online_devices
    
    # Ambil sensor data terbaru per device
    devices = IoTDevice.objects.all()
    sensor_datas = []
    
    for device in devices:
        latest_sensor = SensorData.objects.filter(device=device).order_by('-timestamp').first()
        if latest_sensor:
            sensor_datas.append(latest_sensor)
    
    context = {
        'total_IOTDevice': total_IOTDevice,
        'total_online_devices': total_online_devices,
        'total_offline_devices': total_offline_devices,
        'SensorDatas': sensor_datas,
    }
    return render(request, 'home.html', context)
