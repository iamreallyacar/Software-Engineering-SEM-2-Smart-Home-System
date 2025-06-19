"""
Service layer for device-related business logic.
Handles device control, creation, and energy monitoring.
"""

from api.models.device_models import Device, SupportedDevice
from api.models.home_models import Room


class DeviceService:
    """Service class for device operations"""
    
    @staticmethod
    def get_user_devices(user):
        """Get all devices accessible to a user"""
        return Device.objects.filter(
            room__smart_home__creator=user
        ) | Device.objects.filter(
            room__smart_home__members=user
        )
    
    @staticmethod
    def control_device(device_id, status=None, analogue_value=None):
        """
        Control a device's status and/or analogue value.
        Returns (success: bool, device: Device or None, message: str)
        """
        try:
            device = Device.objects.get(id=device_id)
            
            if status is not None:
                device.status = status
            if analogue_value is not None:
                device.analogue_value = analogue_value
                
            device.save()
            return True, device, "Device updated successfully"
            
        except Device.DoesNotExist:
            return False, None, "Device not found"
    
    @staticmethod
    def add_device_to_room(room_id, supported_device_id, name=None):
        """
        Add a device to a room.
        Returns (success: bool, device: Device or None, message: str)
        """
        try:
            room = Room.objects.get(id=room_id)
            supported_device = SupportedDevice.objects.get(id=supported_device_id)
            
            # Check if device already exists in room
            if Device.objects.filter(room=room, supported_device=supported_device).exists():
                return False, None, "Device already exists in this room"
            
            device_name = name or supported_device.model_name
            device = Device.objects.create(
                name=device_name,
                room=room,
                supported_device=supported_device,
                status=False,
                is_unlocked=True
            )
            
            return True, device, "Device added successfully"
            
        except Room.DoesNotExist:
            return False, None, "Room not found"
        except SupportedDevice.DoesNotExist:
            return False, None, "Supported device not found"
    
    @staticmethod
    def get_device_energy_usage(device_id, date_range=None):
        """
        Get energy usage for a device within a date range.
        Returns energy usage data or None if device not found.
        """
        try:
            device = Device.objects.get(id=device_id)
            # Implementation would depend on specific requirements
            # This is a placeholder for more complex energy calculation logic
            return {"device_id": device_id, "usage": 0.0}
        except Device.DoesNotExist:
            return None
    
    @staticmethod
    def validate_device_access(device_id, user):
        """
        Check if a user has access to control a specific device.
        Returns True if user has access, False otherwise.
        """
        try:
            device = Device.objects.get(id=device_id)
            smart_home = device.room.smart_home
            return user == smart_home.creator or user in smart_home.members.all()
        except Device.DoesNotExist:
            return False
