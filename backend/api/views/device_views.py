from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from api.models.device_models import SupportedDevice, Device
from api.models.home_models import Room
from api.serializers.device_serializers import (
    SupportedDeviceSerializer, DeviceSerializer, 
    DeviceControlSerializer, AddDeviceSerializer
)


class SupportedDeviceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for SupportedDevice (read-only)"""
    queryset = SupportedDevice.objects.all()
    serializer_class = SupportedDeviceSerializer
    permission_classes = [AllowAny]


class DeviceViewSet(viewsets.ModelViewSet):
    """ViewSet for Device CRUD operations"""
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(
            room__smart_home__creator=user
        ) | Device.objects.filter(
            room__smart_home__members=user
        )


class DeviceControlView(APIView):
    """API view for controlling device status and analogue values"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = DeviceControlSerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data['device_id']
            new_status = serializer.validated_data.get('status')
            new_analogue_value = serializer.validated_data.get('analogue_value')
            
            device = get_object_or_404(Device, pk=device_id)
            
            if new_status is not None:
                device.status = new_status
            if new_analogue_value is not None:
                device.analogue_value = new_analogue_value
                
            device.save()
            
            return Response({
                'message': 'Device updated successfully',
                'device_id': device.id,
                'status': device.status,
                'analogue_value': device.analogue_value
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_device_to_room(request):
    """Add a device to a room"""
    serializer = AddDeviceSerializer(data=request.data)
    if serializer.is_valid():
        room_id = serializer.validated_data['room_id']
        supported_device_id = serializer.validated_data['supported_device_id']
        
        room = get_object_or_404(Room, pk=room_id)
        supported_device = get_object_or_404(SupportedDevice, pk=supported_device_id)
        
        # Check that the device is not already in this room
        if Device.objects.filter(room=room, supported_device=supported_device).exists():
            return Response({"detail": "Device already exists in this room."}, status=status.HTTP_400_BAD_REQUEST)
        
        device = Device.objects.create(
            name=f"{supported_device.model_name}",
            room=room,
            supported_device=supported_device,
            status=False,
            is_unlocked=True
        )
        
        return Response({"detail": "Device added", "device_id": device.id}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Legacy compatibility
AddDeviceView = add_device_to_room
