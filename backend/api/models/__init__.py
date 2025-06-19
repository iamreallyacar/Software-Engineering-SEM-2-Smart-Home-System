# Import all models to maintain backward compatibility
from .user_models import UserProfile, RecoveryCode
from .home_models import SmartHome, Room
from .device_models import SupportedDevice, Device
from .log_models import (
    DeviceLog1Min, DeviceLogDaily, DeviceLogMonthly,
    RoomLog1Min, RoomLogDaily, RoomLogMonthly,
    EnergyGeneration1Min, EnergyGenerationDaily, EnergyGenerationMonthly
)

# Re-export for backward compatibility
__all__ = [
    'UserProfile', 'RecoveryCode',
    'SmartHome', 'Room', 
    'SupportedDevice', 'Device',
    'DeviceLog1Min', 'DeviceLogDaily', 'DeviceLogMonthly',
    'RoomLog1Min', 'RoomLogDaily', 'RoomLogMonthly',
    'EnergyGeneration1Min', 'EnergyGenerationDaily', 'EnergyGenerationMonthly'
]
