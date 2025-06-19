from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.db import models
from django.contrib.auth.models import User

from api.models.home_models import SmartHome
from api.models.user_models import UserProfile
from api.serializers.user_serializers import UserSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User CRUD operations"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile CRUD operations"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    """Get current user information"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    """Get current user information (legacy compatibility)"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    """Simple dashboard summary"""
    user = request.user
    smart_homes = SmartHome.objects.filter(
        models.Q(creator=user) | models.Q(members=user)
    ).count()
    
    return Response({
        'smart_homes_count': smart_homes,
        'user': user.username
    })


def home(request):
    """Basic home view"""
    return HttpResponse("Welcome to the Smart Home API")
