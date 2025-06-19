import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models.device_models import Device
from .demo_simulator import DeviceSimulator

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Device)
def log_device_change(sender, instance, **kwargs):
    """
    Log when a device's status or analogue_value changes.
    Enhanced for demonstration purposes with energy impact calculation.
    """
    # Skip for new devices (no pk yet)
    if not instance.pk:
        return
        
    try:
        # Get the original device state from database
        original_device = Device.objects.get(pk=instance.pk)
        
        # Check if status changed
        if original_device.status != instance.status:
            # Calculate energy impact for demo
            old_usage = DeviceSimulator.get_device_energy_usage(original_device)
            original_device.status = instance.status  # Temporarily set new status
            new_usage = DeviceSimulator.get_device_energy_usage(original_device)
            energy_change = new_usage - old_usage
            
            logger.info(
                f"Device {instance.name} status changed from {original_device.status} to {instance.status}. "
                f"Energy impact: {energy_change:+.1f}W"
            )
        
        # Check if analogue_value changed
        if original_device.analogue_value != instance.analogue_value:
            logger.info(
                f"Device {instance.name} analogue value changed from "
                f"{original_device.analogue_value} to {instance.analogue_value}"
            )
            
    except Device.DoesNotExist:
        # Device doesn't exist in DB yet (new device)
        logger.info(f"New device created: {instance.name}")
    except Exception as e:
        logger.error(f"Error in device change signal: {e}")

@receiver(post_save, sender=Device)
def device_demo_feedback(sender, instance, created, **kwargs):
    """
    Provide immediate feedback for demonstration purposes.
    This could be extended to trigger WebSocket notifications in the future.
    """
    if created:
        logger.info(f"✨ Demo: New device '{instance.name}' added to {instance.room.name}")
    else:
        # Calculate current energy usage for context
        current_usage = DeviceSimulator.get_device_energy_usage(instance)
        if current_usage > 0:
            logger.info(f"⚡ Demo: {instance.name} now using {current_usage}W")
        else:
            logger.info(f"💤 Demo: {instance.name} is now off/standby")