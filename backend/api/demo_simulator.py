"""
Simplified device simulation for demonstration purposes.
Replaces the complex scheduled_scripts.py with real-time, on-demand energy calculation.
"""

import random
from django.utils import timezone
from datetime import datetime, timedelta
from .models.device_models import Device
from .models.home_models import SmartHome


class DeviceSimulator:
    """Simple device simulator for demonstration"""
    
    @staticmethod
    def get_device_energy_usage(device):
        """Calculate current energy usage for a device"""
        if not device.status or not device.supported_device.consumption_rate:
            return 0.0
            
        # Base consumption rate (watts)
        base_rate = device.supported_device.consumption_rate
        
        # Add some realistic variation (±10%)
        variation = random.uniform(0.9, 1.1)
        current_usage = base_rate * variation
        
        # For analogue devices, scale by analogue value (0-10)
        if device.analogue_value is not None:
            scale_factor = device.analogue_value / 10.0
            current_usage *= scale_factor
            
        return round(current_usage, 2)
    
    @staticmethod
    def get_room_energy_usage(room):
        """Calculate total energy usage for all devices in a room"""
        total = 0.0
        for device in room.devices.all():
            if device.is_unlocked:
                total += DeviceSimulator.get_device_energy_usage(device)
        return round(total, 2)
    
    @staticmethod
    def get_home_energy_usage(smart_home):
        """Calculate total energy usage for entire home"""
        total = 0.0
        for room in smart_home.rooms.all():
            if room.is_unlocked:
                total += DeviceSimulator.get_room_energy_usage(room)
        return round(total, 2)
    
    @staticmethod
    def get_home_energy_generation(smart_home):
        """Simulate solar panel or other energy generation"""
        # Simulate time-of-day variation for solar panels
        now = timezone.now()
        hour = now.hour
        
        # Peak generation during midday (10am-2pm)
        if 10 <= hour <= 14:
            base_generation = random.uniform(800, 1200)  # Peak watts
        elif 8 <= hour <= 16:
            base_generation = random.uniform(400, 800)   # Good generation
        elif 6 <= hour <= 18:
            base_generation = random.uniform(100, 400)   # Low generation
        else:
            base_generation = 0  # No generation at night
            
        return round(base_generation, 2)
    
    @staticmethod
    def get_energy_efficiency_tips(smart_home):
        """Generate helpful energy tips based on current usage"""
        tips = []
        total_usage = DeviceSimulator.get_home_energy_usage(smart_home)
        
        if total_usage > 1500:
            tips.append("⚡ High energy usage detected. Consider turning off unused devices.")
        
        # Check for devices left on in unoccupied rooms
        for room in smart_home.rooms.all():
            if room.is_unlocked:
                active_devices = room.devices.filter(status=True, is_unlocked=True).count()
                if active_devices > 3:
                    tips.append(f"💡 {room.name} has many devices on. Check if all are needed.")
        
        # Check for energy generation vs consumption
        generation = DeviceSimulator.get_home_energy_generation(smart_home)
        if generation > total_usage:
            tips.append("🌟 Great! Your solar panels are generating more energy than you're using.")
        elif total_usage > generation * 1.5:
            tips.append("🔋 Consider using energy storage or reducing consumption during peak hours.")
            
        return tips


class DemoScenarios:
    """Pre-built scenarios for demonstration"""
    
    @staticmethod
    def create_morning_routine(smart_home):
        """Simulate a typical morning routine"""
        scenarios = [
            ("Living Room", "Main Light", True),
            ("Kitchen", "Coffee Maker", True),
            ("Kitchen", "Main Light", True),
            ("Bathroom", "Main Light", True),
            ("Bathroom", "Exhaust Fan", True),
        ]
        
        applied_count = 0
        for room_name, device_name, status in scenarios:
            try:
                room = smart_home.rooms.get(name=room_name, is_unlocked=True)
                device = room.devices.filter(name__icontains=device_name.split()[0]).first()
                if device and device.is_unlocked:
                    device.status = status
                    device.save()
                    applied_count += 1
            except:
                continue
                
        return f"Applied morning routine: {applied_count} devices activated"
    
    @staticmethod
    def create_energy_saving_mode(smart_home):
        """Turn off non-essential devices"""
        turned_off = 0
        essential_devices = ["security", "refrigerator", "freezer", "alarm"]
        
        for room in smart_home.rooms.filter(is_unlocked=True):
            for device in room.devices.filter(status=True, is_unlocked=True):
                # Keep essential devices on
                if not any(essential in device.name.lower() for essential in essential_devices):
                    device.status = False
                    device.save()
                    turned_off += 1
                    
        return f"Energy saving mode: {turned_off} devices turned off"
    
    @staticmethod
    def simulate_realistic_usage(smart_home):
        """Create realistic device usage patterns"""
        now = timezone.now()
        hour = now.hour
        
        # Morning routine (6-9 AM)
        if 6 <= hour <= 9:
            return DemoScenarios.create_morning_routine(smart_home)
        
        # Evening routine (6-10 PM)
        elif 18 <= hour <= 22:
            scenarios = [
                ("Living Room", "TV", True),
                ("Living Room", "Main Light", True),
                ("Kitchen", "Main Light", True),
                ("Bedroom", "Bedside Lamp", True),
            ]
            
            applied_count = 0
            for room_name, device_name, status in scenarios:
                try:
                    room = smart_home.rooms.get(name=room_name, is_unlocked=True)
                    device = room.devices.filter(name__icontains=device_name.split()[0]).first()
                    if device and device.is_unlocked:
                        device.status = status
                        device.save()
                        applied_count += 1
                except:
                    continue
                    
            return f"Applied evening routine: {applied_count} devices activated"
        
        # Night mode (10 PM - 6 AM)
        elif hour >= 22 or hour <= 6:
            return DemoScenarios.create_energy_saving_mode(smart_home)
        
        # Random daytime activity
        else:
            # Randomly toggle 1-2 devices
            unlocked_devices = []
            for room in smart_home.rooms.filter(is_unlocked=True):
                unlocked_devices.extend(room.devices.filter(is_unlocked=True))
            
            if unlocked_devices:
                device = random.choice(unlocked_devices)
                device.status = not device.status
                device.save()
                return f"Simulated activity: {device.name} {'turned on' if device.status else 'turned off'}"
            
            return "No devices available for simulation"
