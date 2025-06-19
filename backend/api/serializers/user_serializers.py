import re
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models.user_models import UserProfile, RecoveryCode


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'date_of_birth', 'gender', 'phone_number']
        read_only_fields = ['user']


class UserSerializer(serializers.ModelSerializer):
    """Enhanced UserSerializer to handle nested profile updates"""
    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile', 'first_name', 'last_name', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True}
        }
    
    def create(self, validated_data):
        # Extract profile data if present
        profile_data = validated_data.pop('profile', None)
        
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # If profile data was provided, ensure profile exists and update it
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=user)
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()
            
        return user

    def update(self, instance, validated_data):
        # Extract and handle profile data if present
        profile_data = validated_data.pop('profile', None)
        
        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        # Update password if provided
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        
        # Update profile if data was provided
        if profile_data and hasattr(instance, 'profile'):
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        return instance


class RecoveryCodeSerializer(serializers.ModelSerializer):
    """Serializer for the RecoveryCode model"""
    class Meta:
        model = RecoveryCode
        fields = ['code', 'created_at']
        read_only_fields = ['code', 'created_at']


class PasswordResetWithCodeSerializer(serializers.Serializer):
    """Serializer for resetting password with a recovery code"""
    recovery_code = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, 
        min_length=8,
        write_only=True
    )
    
    def validate_recovery_code(self, value):
        """Validate that the recovery code format is correct"""
        # Clean the code format
        value = value.strip()
        
        # Check if it matches the expected format (xxxxx-xxxxx)
        if not re.match(r'^[a-z0-9]{5}-[a-z0-9]{5}$', value):
            raise serializers.ValidationError(
                "Invalid recovery code format. Expected format: xxxxx-xxxxx"
            )
        
        # Code format is valid
        return value
        
    def validate_new_password(self, value):
        """Validate that the new password meets security requirements"""
        # Check for minimum complexity
        if value.isdigit():
            raise serializers.ValidationError(
                "Password cannot be entirely numeric."
            )
            
        return value
