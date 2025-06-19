from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import models

from api.models.home_models import SmartHome, Room
from api.serializers.home_serializers import (
    SmartHomeSerializer, RoomSerializer, SmartHomeListSerializer, 
    JoinHomeSerializer, UnlockRoomSerializer
)


class SmartHomeViewSet(viewsets.ModelViewSet):
    """ViewSet for SmartHome CRUD operations"""
    queryset = SmartHome.objects.all()
    serializer_class = SmartHomeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return SmartHome.objects.filter(
            models.Q(creator=user) | models.Q(members=user)
        ).distinct()


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet for Room CRUD operations"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(
            smart_home__creator=user
        ) | Room.objects.filter(
            smart_home__members=user
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_smarthome(request):
    """Create a new smart home"""
    name = request.data.get('name')
    join_password = request.data.get('join_password', '')
    
    if not name:
        return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    smart_home = SmartHome.objects.create(
        name=name,
        creator=request.user,
        join_password=join_password
    )
    
    return Response({
        'message': 'Smart home created successfully',
        'smart_home_id': smart_home.id,
        'name': smart_home.name
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_smart_home(request):
    """Join an existing smart home using name and password"""
    serializer = JoinHomeSerializer(data=request.data)
    if serializer.is_valid():
        home_name = serializer.validated_data['home_name']
        password = serializer.validated_data['password']
        
        try:
            smart_home = SmartHome.objects.get(name=home_name, join_password=password)
            smart_home.members.add(request.user)
            return Response({'message': 'Successfully joined smart home'}, status=status.HTTP_200_OK)
        except SmartHome.DoesNotExist:
            return Response({'error': 'Invalid home name or password'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_smarthome(request):
    """Leave a smart home"""
    smart_home_id = request.data.get('smart_home_id')
    
    if not smart_home_id:
        return Response({'error': 'Smart home ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        smart_home = SmartHome.objects.get(id=smart_home_id)
        smart_home.members.remove(request.user)
        return Response({'message': 'Successfully left smart home'}, status=status.HTTP_200_OK)
    except SmartHome.DoesNotExist:
        return Response({'error': 'Smart home not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_smarthome_members(request):
    """Get all members of a smart home"""
    smart_home_id = request.GET.get('smart_home_id')
    
    if not smart_home_id:
        return Response({'error': 'Smart home ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        smart_home = SmartHome.objects.get(id=smart_home_id)
        members = [{'id': user.id, 'username': user.username} for user in smart_home.members.all()]
        creator = {'id': smart_home.creator.id, 'username': smart_home.creator.username}
        
        return Response({
            'creator': creator,
            'members': members
        }, status=status.HTTP_200_OK)
    except SmartHome.DoesNotExist:
        return Response({'error': 'Smart home not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlock_room(request):
    """Unlock a room in a smart home"""
    serializer = UnlockRoomSerializer(data=request.data)
    if serializer.is_valid():
        smart_home_id = serializer.validated_data['smart_home_id']
        room_id = serializer.validated_data['room_id']
        
        smart_home = get_object_or_404(SmartHome, pk=smart_home_id)
        room = get_object_or_404(Room, pk=room_id, smart_home=smart_home)
        
        if room.is_unlocked:
            return Response({"detail": "Room already unlocked"}, status=status.HTTP_400_BAD_REQUEST)
        
        room.is_unlocked = True
        room.save()
        
        return Response({"detail": "Room unlocked", "room_id": room.id}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Legacy compatibility
UnlockRoomView = unlock_room
