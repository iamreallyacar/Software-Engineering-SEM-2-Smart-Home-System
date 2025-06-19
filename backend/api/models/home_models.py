from django.db import models
from django.contrib.auth.models import User


class SmartHome(models.Model):
    """
    A smart home in our system that users can create and join.
    
    Think of this as the virtual representation of a physical house, connecting
    all the rooms, devices, and users together. Each home has an owner (creator) 
    and can have multiple members who can access and control the home's features.
    
    The join_password allows other users to join this home by providing the password.
    """
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_homes')
    members = models.ManyToManyField(User, related_name='joined_homes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    join_password = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    """
    A room within a smart home where devices can be placed.
    
    Rooms serve as organizational units for grouping related devices (like a real 
    bedroom or kitchen would contain specific appliances).
    
    The is_unlocked field determines if users can access and control this room,
    implementing our progressive unlocking feature.
    """
    name = models.CharField(max_length=255)
    smart_home = models.ForeignKey(SmartHome, on_delete=models.CASCADE, related_name='rooms')
    is_unlocked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'smart_home'], name='unique_room_in_home')
        ]

    def __str__(self):
        return f"{self.name} (Home: {self.smart_home.name})"
