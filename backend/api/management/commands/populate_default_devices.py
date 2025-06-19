# Management command to populate default supported devices
# Run with: python manage.py populate_default_devices

from django.core.management.base import BaseCommand
from api.models.device_models import SupportedDevice


class Command(BaseCommand):
    help = 'Populate default supported devices for the smart home system'

    def handle(self, *args, **options):
        default_devices = [
            {
                'model_name': 'Smart Light Bulb',
                'type': 'lighting',
                'number': 1,
                'consumption_rate': 10,
            },
            {
                'model_name': 'Smart Switch',
                'type': 'switch',
                'number': 2,
                'consumption_rate': 5,
            },
            {
                'model_name': 'Smart Thermostat',
                'type': 'heating',
                'number': 3,
                'consumption_rate': 150,
            },
            {
                'model_name': 'Motion Sensor',
                'type': 'sensor',
                'number': 4,
                'consumption_rate': 2,
            },
            {
                'model_name': 'Smart Lock',
                'type': 'security',
                'number': 5,
                'consumption_rate': 8,
            },
            {
                'model_name': 'Smart Doorbell',
                'type': 'security',
                'number': 6,
                'consumption_rate': 15,
            },
            {
                'model_name': 'Smart TV',
                'type': 'entertainment',
                'number': 7,
                'consumption_rate': 200,
            },
            {
                'model_name': 'Smart Speaker',
                'type': 'entertainment',
                'number': 8,
                'consumption_rate': 25,
            },
            {
                'model_name': 'Smart Fan',
                'type': 'climate',
                'number': 9,
                'consumption_rate': 75,
            },
            {
                'model_name': 'Smart Garage Door',
                'type': 'access',
                'number': 10,
                'consumption_rate': 300,
            },
        ]

        created_count = 0
        for device_data in default_devices:
            device, created = SupportedDevice.objects.get_or_create(
                model_name=device_data['model_name'],
                defaults=device_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created device: {device.model_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Device already exists: {device.model_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nPopulation complete! Created {created_count} new devices.')
        )
