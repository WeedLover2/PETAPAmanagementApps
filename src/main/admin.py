from django.contrib import admin
from .models import IoTDevice, SensorData

@admin.register(IoTDevice)
class IoTDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'last_active', 'is_active', 'status']
    list_filter = ['is_active']
    search_fields = ['device_id', 'name']
    readonly_fields = ['last_active', 'status']
    list_per_page = 20

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['device', 'is_smoke_detected', 'is_vibration_detected', 'timestamp']
    list_filter = ['device', 'is_smoke_detected', 'is_vibration_detected']
    search_fields = ['device__device_id', 'device__name']
    readonly_fields = ['timestamp']
    list_per_page = 50
    date_hierarchy = 'timestamp'

