from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models.home_models import SmartHome, Room
from .models.user_models import UserProfile
from .models.device_models import SupportedDevice, Device

@receiver(post_save, sender=SmartHome)
def create_demo_home_layout(sender, instance, created, **kwargs):
    """
    When a new SmartHome is created, this signal handler creates a demo-ready layout
    with default rooms and some basic devices for demonstration purposes.
    """
    if created:
        # Create default rooms for the new smart home
        default_rooms = [
            {"name": "Living Room", "unlock_order": 1},
            {"name": "Kitchen", "unlock_order": 2},
            {"name": "Bedroom", "unlock_order": 3},
            {"name": "Bathroom", "unlock_order": 4},
            {"name": "Garden", "unlock_order": 5},
        ]
        
        created_rooms = {}
        for room_data in default_rooms:
            room = Room.objects.create(
                name=room_data["name"],
                smart_home=instance,
                is_unlocked=(room_data["unlock_order"] == 1)  # Only first room unlocked initially
            )
            created_rooms[room_data["name"]] = room
        
        # Add some demo devices to the Living Room to make it interesting
        if "Living Room" in created_rooms:
            living_room = created_rooms["Living Room"]
            
            # Try to get or create some basic supported devices for demo
            demo_devices = [
                {"type": "Light", "name": "Main Light", "consumption": 60},
                {"type": "Entertainment", "name": "TV", "consumption": 150},
                {"type": "Climate", "name": "Fan", "consumption": 75},
            ]
            
            for device_info in demo_devices:
                # Get or create the supported device type
                supported_device, _ = SupportedDevice.objects.get_or_create(
                    type=device_info["type"],
                    defaults={
                        'consumption_rate': device_info["consumption"],
                        'number': 1  # Default quantity
                    }
                )
                
                # Create the actual device in the room
                Device.objects.create(
                    name=device_info["name"],
                    supported_device=supported_device,
                    room=living_room,
                    status=False,  # Start with devices off
                    is_unlocked=True
                )

# Signal to create UserProfile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    When a new User is created, this signal handler creates a UserProfile for them.
    """
    if created:
        UserProfile.objects.create(user=instance)