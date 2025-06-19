from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models.home_models import SmartHome, Room
from api.models.device_models import Device, SupportedDevice


class Command(BaseCommand):
    help = 'Create demo data for the smart home system'

    def handle(self, *args, **options):
        # Create demo user
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
            }
        )
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created demo user: {user.username}'))
        else:
            self.stdout.write(f'Demo user already exists: {user.username}')

        # Create demo smart home
        smart_home, created = SmartHome.objects.get_or_create(
            name='Demo Smart Home',
            creator=user,
            defaults={
                'join_password': 'demo123'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created smart home: {smart_home.name}'))
        else:
            self.stdout.write(f'Smart home already exists: {smart_home.name}')

        # Create demo rooms
        rooms_data = [
            {'name': 'Living Room', 'is_unlocked': True},
            {'name': 'Kitchen', 'is_unlocked': True},
            {'name': 'Bedroom', 'is_unlocked': False},
            {'name': 'Bathroom', 'is_unlocked': False},
            {'name': 'Garage', 'is_unlocked': False},
        ]

        rooms = []
        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                name=room_data['name'],
                smart_home=smart_home,
                defaults={'is_unlocked': room_data['is_unlocked']}
            )
            rooms.append(room)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created room: {room.name}'))
            else:
                self.stdout.write(f'Room already exists: {room.name}')

        # Get supported devices
        supported_devices = list(SupportedDevice.objects.all())
        if not supported_devices:
            self.stdout.write(self.style.ERROR('No supported devices found. Run populate_default_devices first.'))
            return

        # Create demo devices
        devices_data = [
            {'name': 'Living Room Light', 'room': 'Living Room', 'device_type': 'Smart Light Bulb', 'status': True, 'analogue_value': 75},
            {'name': 'Living Room TV', 'room': 'Living Room', 'device_type': 'Smart TV', 'status': False, 'analogue_value': 50},
            {'name': 'Kitchen Light', 'room': 'Kitchen', 'device_type': 'Smart Light Bulb', 'status': True, 'analogue_value': 100},
            {'name': 'Kitchen Fan', 'room': 'Kitchen', 'device_type': 'Smart Fan', 'status': False, 'analogue_value': 0},
            {'name': 'Bedroom Light', 'room': 'Bedroom', 'device_type': 'Smart Light Bulb', 'status': False, 'analogue_value': 0},
            {'name': 'Bedroom Speaker', 'room': 'Bedroom', 'device_type': 'Smart Speaker', 'status': False, 'analogue_value': 30},
            {'name': 'Bathroom Light', 'room': 'Bathroom', 'device_type': 'Smart Light Bulb', 'status': False, 'analogue_value': 0},
            {'name': 'Garage Door', 'room': 'Garage', 'device_type': 'Smart Garage Door', 'status': False, 'analogue_value': None},
            {'name': 'Main Door Lock', 'room': 'Living Room', 'device_type': 'Smart Lock', 'status': True, 'analogue_value': None},
        ]

        for device_data in devices_data:
            room = next((r for r in rooms if r.name == device_data['room']), None)
            supported_device = next((sd for sd in supported_devices if sd.model_name == device_data['device_type']), None)
            
            if not room or not supported_device:
                self.stdout.write(self.style.WARNING(f'Skipping device {device_data["name"]} - room or device type not found'))
                continue

            device, created = Device.objects.get_or_create(
                name=device_data['name'],
                room=room,
                supported_device=supported_device,
                defaults={
                    'status': device_data['status'],
                    'analogue_value': device_data['analogue_value'],
                    'is_unlocked': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created device: {device.name} in {room.name}'))
            else:
                self.stdout.write(f'Device already exists: {device.name}')

        self.stdout.write(self.style.SUCCESS('\nDemo data creation complete!'))
        self.stdout.write('\nDemo credentials:')
        self.stdout.write(f'  Username: demo')
        self.stdout.write(f'  Password: demo123')
        self.stdout.write(f'  Smart Home: {smart_home.name}')
        self.stdout.write(f'  Join Password: demo123')
