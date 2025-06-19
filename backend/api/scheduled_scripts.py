"""
Simplified background tasks for demonstration purposes.
This file replaces the complex scheduled scripts with basic demo functionality.
Real-time energy calculation is primarily handled by demo_simulator.py
"""

import random
from django.utils import timezone
from datetime import timedelta
from .models.home_models import SmartHome
from .models.device_models import Device
from .models.log_models import DeviceLog1Min, EnergyGeneration1Min


def generate_demo_energy_snapshot():
    """
    Generate a single energy snapshot for demo purposes.
    This creates basic logging data for demonstration without complex aggregation.
    """
    current_time = timezone.now().replace(second=0, microsecond=0)
    
    # Generate basic energy generation for all homes
    homes = SmartHome.objects.all()
    for home in homes:
        # Simple solar generation simulation based on time of day
        hour = current_time.hour
        if 6 <= hour <= 18:  # Daylight hours
            base_generation = 500  # Base watts
            # Add time-of-day variation
            if 10 <= hour <= 14:  # Peak hours
                generation = base_generation + random.uniform(200, 500)
            else:
                generation = base_generation + random.uniform(0, 200)
        else:
            generation = 0  # No generation at night
            
        EnergyGeneration1Min.objects.create(
            home=home,
            energy_generation=generation / 1000 / 60,  # Convert to kWh for 1 minute
            created_at=current_time
        )
    
    # Log current device states (simplified)
    active_devices = Device.objects.filter(status=True, is_unlocked=True)
    logged_count = 0
    
    for device in active_devices:
        if device.supported_device.consumption_rate:
            # Convert watts to kWh for 1 minute
            energy_kwh = device.supported_device.consumption_rate / 1000 / 60
            
            # Add some realistic variation
            variation = random.uniform(0.9, 1.1)
            energy_kwh *= variation
            
            DeviceLog1Min.objects.create(
                device=device,
                status=device.status,
                energy_usage=energy_kwh,
                created_at=current_time
            )
            logged_count += 1
    
    return f"Demo snapshot: {len(homes)} homes, {logged_count} active devices logged"


def cleanup_old_demo_logs(hours_to_keep=24):
    """
    Clean up old demo logs to prevent database bloat.
    Keep only recent data for demo purposes.
    """
    cutoff_time = timezone.now() - timedelta(hours=hours_to_keep)
    
    # Clean up old device logs
    deleted_device_logs = DeviceLog1Min.objects.filter(created_at__lt=cutoff_time).delete()
    
    # Clean up old energy generation logs
    deleted_energy_logs = EnergyGeneration1Min.objects.filter(created_at__lt=cutoff_time).delete()
    
    return f"Cleanup completed: {deleted_device_logs[0]} device logs and {deleted_energy_logs[0]} energy logs removed"


def get_recent_energy_trends(smart_home, hours=2):
    """
    Get recent energy trends for demonstration charts.
    Returns data points for the last few hours.
    """
    end_time = timezone.now()
    start_time = end_time - timedelta(hours=hours)
    
    # Get energy generation data
    generation_logs = EnergyGeneration1Min.objects.filter(
        home=smart_home,
        created_at__gte=start_time,
        created_at__lte=end_time
    ).order_by('created_at')
    
    # Get device consumption data
    device_logs = DeviceLog1Min.objects.filter(
        device__room__smart_home=smart_home,
        created_at__gte=start_time,
        created_at__lte=end_time
    ).order_by('created_at')
    
    # Group by minute for charting
    energy_data = []
    consumption_data = []
    
    # Process generation data
    for log in generation_logs:
        energy_data.append({
            'timestamp': log.created_at.isoformat(),
            'generation_kwh': log.energy_generation * 1000,  # Convert back to watts for display
        })
    
    # Aggregate consumption by minute
    consumption_by_minute = {}
    for log in device_logs:
        minute_key = log.created_at.replace(second=0, microsecond=0)
        if minute_key not in consumption_by_minute:
            consumption_by_minute[minute_key] = 0
        consumption_by_minute[minute_key] += log.energy_usage * 1000  # Convert to watts
    
    for timestamp, consumption in consumption_by_minute.items():
        consumption_data.append({
            'timestamp': timestamp.isoformat(),
            'consumption_watts': consumption
        })
    
    return {
        'period_hours': hours,
        'generation_data': energy_data,
        'consumption_data': consumption_data,
        'data_points': len(energy_data) + len(consumption_data)
    }


def simulate_demo_activity(smart_home):
    """
    Simulate some demo activity by randomly toggling a few devices.
    This creates realistic activity for demonstration purposes.
    """
    # Get some unlocked devices
    available_devices = Device.objects.filter(
        room__smart_home=smart_home,
        room__is_unlocked=True,
        is_unlocked=True
    )
    
    if not available_devices.exists():
        return "No devices available for simulation"
    
    # Toggle 1-3 devices randomly
    num_to_toggle = min(random.randint(1, 3), available_devices.count())
    devices_to_toggle = random.sample(list(available_devices), num_to_toggle)
    
    changes = []
    for device in devices_to_toggle:
        old_status = device.status
        device.status = not device.status
        device.save()
        
        changes.append(f"{device.name}: {'ON' if device.status else 'OFF'}")
    
    return f"Demo activity: {', '.join(changes)}"


# Keep this minimal - the main energy calculations are now in demo_simulator.py
# These functions are kept for any remaining background logging needs