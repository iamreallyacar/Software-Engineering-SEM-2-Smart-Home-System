"""
API views for demonstration features.
Provides real-time energy monitoring and demo scenarios.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.models.home_models import SmartHome, Room
from api.models.device_models import Device
from api.demo_simulator import DeviceSimulator, DemoScenarios
from api.services.home_service import SmartHomeService
from api.scheduled_scripts import get_recent_energy_trends, simulate_demo_activity


def get_user_smart_home(user):
    """
    Helper function to get the user's first smart home.
    For demo purposes, we assume users typically have one home.
    """
    homes = SmartHomeService.get_user_homes(user)
    return homes.first() if homes.exists() else None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def real_time_energy_dashboard(request):
    """
    Get real-time energy usage and generation for the user's smart home.
    Returns current consumption, generation, and efficiency tips.
    """
    try:
        user_home = get_user_smart_home(request.user)
        if not user_home:
            return Response(
                {"error": "User is not associated with any smart home"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get real-time energy data
        total_consumption = DeviceSimulator.get_home_energy_usage(user_home)
        total_generation = DeviceSimulator.get_home_energy_generation(user_home)
        efficiency_tips = DeviceSimulator.get_energy_efficiency_tips(user_home)
        
        # Get room-by-room breakdown
        room_breakdown = []
        for room in user_home.rooms.filter(is_unlocked=True):
            room_usage = DeviceSimulator.get_room_energy_usage(room)
            room_devices = []
            
            for device in room.devices.filter(is_unlocked=True):
                device_usage = DeviceSimulator.get_device_energy_usage(device)
                room_devices.append({
                    'id': device.id,
                    'name': device.name,
                    'status': device.status,
                    'current_usage_watts': device_usage,
                    'analogue_value': device.analogue_value
                })
            
            room_breakdown.append({
                'id': room.id,
                'name': room.name,
                'total_usage_watts': room_usage,
                'devices': room_devices
            })
        
        return Response({
            'timestamp': user_home.created_at,
            'home_summary': {
                'total_consumption_watts': total_consumption,
                'total_generation_watts': total_generation,
                'net_consumption_watts': round(total_consumption - total_generation, 2),
                'efficiency_score': min(100, max(0, 100 - (total_consumption / 10))),  # Simple score
            },
            'room_breakdown': room_breakdown,
            'efficiency_tips': efficiency_tips,
            'demo_mode': True
        })
        
    except Exception as e:
        return Response(
            {"error": f"Failed to get energy dashboard: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_demo_scenario(request):
    """
    Run a predefined demo scenario.
    Scenarios: 'morning_routine', 'energy_saving', 'realistic_usage'
    """
    try:
        scenario_type = request.data.get('scenario')
        if not scenario_type:
            return Response(
                {"error": "Scenario type is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_home = get_user_smart_home(request.user)
        if not user_home:
            return Response(
                {"error": "User is not associated with any smart home"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Run the requested scenario
        if scenario_type == 'morning_routine':
            result = DemoScenarios.create_morning_routine(user_home)
        elif scenario_type == 'energy_saving':
            result = DemoScenarios.create_energy_saving_mode(user_home)
        elif scenario_type == 'realistic_usage':
            result = DemoScenarios.simulate_realistic_usage(user_home)
        else:
            return Response(
                {"error": "Invalid scenario type. Use: morning_routine, energy_saving, or realistic_usage"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get updated energy data after scenario
        new_consumption = DeviceSimulator.get_home_energy_usage(user_home)
        new_generation = DeviceSimulator.get_home_energy_generation(user_home)
        
        return Response({
            'scenario': scenario_type,
            'result': result,
            'updated_energy': {
                'total_consumption_watts': new_consumption,
                'total_generation_watts': new_generation,
                'net_consumption_watts': round(new_consumption - new_generation, 2)
            }
        })
        
    except Exception as e:
        return Response(
            {"error": f"Failed to run scenario: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def device_energy_details(request, device_id):
    """
    Get detailed energy information for a specific device.
    Includes historical simulation and efficiency recommendations.
    """
    try:
        device = get_object_or_404(Device, pk=device_id)
        
        # Verify user has access to this device
        user_home = get_user_smart_home(request.user)
        if device.room.smart_home != user_home:
            return Response(
                {"error": "Access denied to this device"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        current_usage = DeviceSimulator.get_device_energy_usage(device)
        
        # Simulate daily usage patterns
        daily_usage_pattern = []
        for hour in range(24):
            # Simulate usage variation throughout the day
            if device.supported_device.consumption_rate:
                base_rate = device.supported_device.consumption_rate
                if device.status:
                    # Add realistic hourly variation
                    if 6 <= hour <= 22:  # Active hours
                        simulated_usage = base_rate * (0.8 + (hour % 6) * 0.1)
                    else:  # Night hours
                        simulated_usage = base_rate * 0.3
                else:
                    simulated_usage = base_rate * 0.1  # Standby power
            else:
                simulated_usage = 0
                
            daily_usage_pattern.append({
                'hour': hour,
                'usage_watts': round(simulated_usage, 2)
            })
        
        # Generate device-specific tips
        device_tips = []
        if current_usage > 100:
            device_tips.append(f"💡 {device.name} is using significant power. Consider reducing usage when not needed.")
        if device.analogue_value and device.analogue_value > 7:
            device_tips.append(f"🔧 {device.name} is set to high intensity. Lower settings can save energy.")
        if device.status and "light" in device.name.lower():
            device_tips.append("🌞 Consider using natural lighting during daytime hours.")
        
        return Response({
            'device': {
                'id': device.id,
                'name': device.name,
                'type': device.supported_device.type,
                'room': device.room.name,
                'status': device.status,
                'analogue_value': device.analogue_value
            },
            'energy_info': {
                'current_usage_watts': current_usage,
                'max_consumption_rate': device.supported_device.consumption_rate,
                'daily_cost_estimate': round(current_usage * 24 * 0.12 / 1000, 2),  # Rough estimate at $0.12/kWh
                'daily_usage_pattern': daily_usage_pattern
            },
            'recommendations': device_tips
        })
        
    except Exception as e:
        return Response(
            {"error": f"Failed to get device details: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([])  # Allow anonymous access for demo purposes
def available_demo_scenarios(request):
    """
    List all available demo scenarios with descriptions.
    """
    scenarios = [
        {
            'id': 'morning_routine',
            'name': 'Morning Routine',
            'description': 'Simulate a typical morning by turning on lights, coffee maker, and bathroom fan',
            'estimated_devices': 5,
            'category': 'lifestyle'
        },
        {
            'id': 'energy_saving',
            'name': 'Energy Saving Mode',
            'description': 'Turn off non-essential devices to reduce energy consumption',
            'estimated_devices': 'varies',
            'category': 'efficiency'
        },
        {
            'id': 'realistic_usage',
            'name': 'Time-based Usage',
            'description': 'Simulate realistic device usage based on current time of day',
            'estimated_devices': 'varies',
            'category': 'simulation'
        }
    ]
    
    return Response({
        'scenarios': scenarios,
        'demo_mode': True
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def energy_trends_chart(request):
    """
    Get energy trends data for charting in the frontend.
    Returns recent consumption and generation data points.
    """
    try:
        user_home = get_user_smart_home(request.user)
        if not user_home:
            return Response(
                {"error": "User is not associated with any smart home"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        hours = int(request.GET.get('hours', 2))  # Default 2 hours
        trends_data = get_recent_energy_trends(user_home, hours)
        
        return Response({
            'home_id': user_home.id,
            'trends': trends_data,
            'demo_mode': True
        })
        
    except Exception as e:
        return Response(
            {"error": f"Failed to get energy trends: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def simulate_activity(request):
    """
    Simulate random device activity for demonstration purposes.
    """
    try:
        user_home = get_user_smart_home(request.user)
        if not user_home:
            return Response(
                {"error": "User is not associated with any smart home"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        result = simulate_demo_activity(user_home)
        
        # Get updated energy consumption after simulation
        new_consumption = DeviceSimulator.get_home_energy_usage(user_home)
        
        return Response({
            'simulation_result': result,
            'updated_consumption_watts': new_consumption,
            'demo_mode': True
        })
        
    except Exception as e:
        return Response(
            {"error": f"Failed to simulate activity: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
