from rest_framework import serializers
from api.models.home_models import SmartHome, Room


class SmartHomeSerializer(serializers.ModelSerializer):
    """Enhanced SmartHomeSerializer to validate members"""
    is_creator = serializers.SerializerMethodField()
    
    class Meta:
        model = SmartHome
        fields = ['id', 'name', 'creator', 'members', 'join_password', 'created_at', 'updated_at', 'is_creator']
        read_only_fields = ['creator', 'created_at', 'updated_at', 'is_creator']
    
    def get_is_creator(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.creator == request.user
        return False

    def get_member_count(self, obj):
        return obj.members.count()

    def validate_members(self, value):
        """Check that the creator is not in the members list"""
        request = self.context.get('request')
        
        # For create operations, the creator will be the current user
        if self.instance is None and request:
            creator = request.user
            if creator in value:
                raise serializers.ValidationError("The creator cannot be added as a member")
        
        # For update operations, check against the existing creator
        elif self.instance:
            creator = self.instance.creator
            if creator in value:
                raise serializers.ValidationError("The creator cannot be added as a member")
                
        return value
        
    def create(self, validated_data):
        # Ensure members doesn't contain the creator
        if 'members' in validated_data:
            members = validated_data.get('members', [])
            creator = self.context['request'].user
            if creator in members:
                members.remove(creator)
            
        # Set creator to current user
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class SmartHomeListSerializer(SmartHomeSerializer):
    """Serializer for listing smart homes (hides join password)"""
    class Meta(SmartHomeSerializer.Meta):
        extra_kwargs = {
            'join_password': {'write_only': True}
        }


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model with daily usage calculation"""
    devices = serializers.StringRelatedField(many=True, read_only=True)  # Simple representation to avoid circular imports
    daily_usage = serializers.SerializerMethodField()
    smart_home_name = serializers.CharField(source='smart_home.name', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'smart_home', 'smart_home_name', 'devices', 'daily_usage', 'is_unlocked']

    def get_daily_usage(self, obj):
        from django.utils import timezone
        from django.db import models
        from api.models.log_models import RoomLog1Min
        
        today = timezone.now().date()
        logs = RoomLog1Min.objects.filter(room=obj, created_at__date=today)
        total_usage = logs.aggregate(models.Sum('energy_usage'))['energy_usage__sum'] or 0
        return total_usage


class JoinHomeSerializer(serializers.Serializer):
    """Serializer for joining a smart home"""
    home_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UnlockRoomSerializer(serializers.Serializer):
    """Serializer for unlocking a room"""
    smart_home_id = serializers.IntegerField()
    room_id = serializers.IntegerField()
