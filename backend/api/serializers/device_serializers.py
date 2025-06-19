from rest_framework import serializers
from api.models.device_models import SupportedDevice, Device


class SupportedDeviceSerializer(serializers.ModelSerializer):
    """Serializer for the SupportedDevice model"""
    class Meta:
        model = SupportedDevice
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    """Serializer for the Device model"""
    class Meta:
        model = Device
        fields = '__all__'


class DeviceControlSerializer(serializers.Serializer):
    """Serializer for controlling device status and analogue values"""
    device_id = serializers.IntegerField(required=True)
    status = serializers.BooleanField(required=False)
    analogue_value = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10
    )
    
    def validate(self, data):
        """Check that at least one of status or analogue_value is provided"""
        if 'status' not in data and 'analogue_value' not in data:
            raise serializers.ValidationError(
                "Either status or analogue_value must be provided"
            )
        return data


class AddDeviceSerializer(serializers.Serializer):
    """Serializer for adding a device to a room"""
    room_id = serializers.IntegerField()
    supported_device_id = serializers.IntegerField()


class UnlockRoomSerializer(serializers.Serializer):
    """Serializer for unlocking a room"""
    smart_home_id = serializers.IntegerField()
    room_id = serializers.IntegerField()
