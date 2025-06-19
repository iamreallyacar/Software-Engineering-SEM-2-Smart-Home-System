from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .home_models import Room


class SupportedDevice(models.Model):
    """
    The definition of a device type that can be installed in our system.
    
    This is like a "template" or "blueprint" for actual devices. It defines
    what kinds of devices our system supports.
    """
    model_name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, default=None, null=True)
    number = models.IntegerField(default=None, null=True)
    consumption_rate = models.IntegerField(null=True, default=None)

    def __str__(self):
        return f"{self.model_name} ({self.type})"


class Device(models.Model):
    """
    An actual device instance installed in a room of a smart home.
    
    While SupportedDevice defines what kinds of devices exist,
    this model represents a specific device that's been placed in a room
    and can be controlled by users.
    
    For example, "Living Room Light" would be a Device instance of a
    "Light Switch" SupportedDevice type.
    
    Devices track their current status (on/off), analog value (0-10 for dimmable
    devices), and when they were created or last updated.
    """
    name = models.CharField(max_length=100)                             
    status = models.BooleanField(default=False)                     
    analogue_value = models.IntegerField(
        null=True, 
        default=None,
        validators=[
            MinValueValidator(0, message="Value must be at least 0"),
            MaxValueValidator(10, message="Value cannot be greater than 10")
        ]
    ) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='devices', null=True) 
    supported_device = models.ForeignKey(SupportedDevice, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)                
    updated_at = models.DateTimeField(auto_now=True)                    
    is_unlocked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'room'], name='unique_device_in_room')
        ]

    def __str__(self):
        return f"{self.name} in {self.room.name}"
