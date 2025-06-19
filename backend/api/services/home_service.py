"""
Service layer for smart home and room-related business logic.
Handles operations like creating homes, managing memberships, and room unlocking.
"""

from django.db import models
from api.models.home_models import SmartHome, Room


class SmartHomeService:
    """Service class for smart home operations"""
    
    @staticmethod
    def create_smart_home(name, creator, join_password=''):
        """Create a new smart home with default rooms"""
        smart_home = SmartHome.objects.create(
            name=name,
            creator=creator,
            join_password=join_password
        )
        # Default rooms are created via signals
        return smart_home
    
    @staticmethod
    def get_user_homes(user):
        """Get all smart homes where user is creator or member"""
        return SmartHome.objects.filter(
            models.Q(creator=user) | models.Q(members=user)
        ).distinct()
    
    @staticmethod
    def join_home(user, home_name, password):
        """
        Join a smart home using name and password.
        Returns (success: bool, message: str)
        """
        try:
            smart_home = SmartHome.objects.get(name=home_name, join_password=password)
            if user == smart_home.creator:
                return False, "You are already the creator of this home"
            if user in smart_home.members.all():
                return False, "You are already a member of this home"
            
            smart_home.members.add(user)
            return True, "Successfully joined smart home"
        except SmartHome.DoesNotExist:
            return False, "Invalid home name or password"
    
    @staticmethod
    def leave_home(user, smart_home_id):
        """
        Leave a smart home.
        Returns (success: bool, message: str)
        """
        try:
            smart_home = SmartHome.objects.get(id=smart_home_id)
            if user == smart_home.creator:
                return False, "Creators cannot leave their own homes"
            
            smart_home.members.remove(user)
            return True, "Successfully left smart home"
        except SmartHome.DoesNotExist:
            return False, "Smart home not found"
    
    @staticmethod
    def get_home_members(smart_home_id):
        """
        Get all members and creator of a smart home.
        Returns (success: bool, data: dict, message: str)
        """
        try:
            smart_home = SmartHome.objects.get(id=smart_home_id)
            members = [{'id': user.id, 'username': user.username} for user in smart_home.members.all()]
            creator = {'id': smart_home.creator.id, 'username': smart_home.creator.username}
            
            return True, {'creator': creator, 'members': members}, ""
        except SmartHome.DoesNotExist:
            return False, {}, "Smart home not found"


class RoomService:
    """Service class for room operations"""
    
    @staticmethod
    def get_user_rooms(user):
        """Get all rooms accessible to a user"""
        return Room.objects.filter(
            smart_home__creator=user
        ) | Room.objects.filter(
            smart_home__members=user
        )
    
    @staticmethod
    def unlock_room(smart_home_id, room_id):
        """
        Unlock a room in a smart home.
        Returns (success: bool, message: str, room_id: int or None)
        """
        try:
            smart_home = SmartHome.objects.get(id=smart_home_id)
            room = Room.objects.get(id=room_id, smart_home=smart_home)
            
            if room.is_unlocked:
                return False, "Room already unlocked", None
            
            room.is_unlocked = True
            room.save()
            return True, "Room unlocked", room.id
            
        except SmartHome.DoesNotExist:
            return False, "Smart home not found", None
        except Room.DoesNotExist:
            return False, "Room not found", None
    
    @staticmethod
    def get_room_daily_usage(room):
        """Calculate daily energy usage for a room"""
        from django.utils import timezone
        from django.db import models
        from api.models.log_models import RoomLog1Min
        
        today = timezone.now().date()
        logs = RoomLog1Min.objects.filter(room=room, created_at__date=today)
        total_usage = logs.aggregate(models.Sum('energy_usage'))['energy_usage__sum'] or 0
        return total_usage
