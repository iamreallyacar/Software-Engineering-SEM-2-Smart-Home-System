"""
Service layer for authentication-related business logic.
Separates business rules from API views for better testability and reusability.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models.user_models import RecoveryCode, UserProfile


class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate a user with username and password.
        Returns user object if successful, None if failed.
        """
        return authenticate(username=username, password=password)
    
    @staticmethod
    def create_user_token(user):
        """Create or get authentication token for user"""
        token, created = Token.objects.get_or_create(user=user)
        return token
    
    @staticmethod
    def revoke_user_token(user):
        """Revoke user's authentication token"""
        try:
            user.auth_token.delete()
            return True
        except:
            return False
    
    @staticmethod
    def register_user(username, email, password, first_name='', last_name=''):
        """
        Register a new user and create their profile.
        Returns the created user object.
        """
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # UserProfile is created automatically via signals
        return user


class RecoveryCodeService:
    """Service class for recovery code operations"""
    
    @staticmethod
    def generate_codes_for_user(user, count=10):
        """Generate new recovery codes for a user"""
        return RecoveryCode.create_for_user(user, count)
    
    @staticmethod
    def get_user_codes(user):
        """Get all recovery codes for a user"""
        return RecoveryCode.objects.filter(user=user)
    
    @staticmethod
    def validate_and_use_code(code, new_password):
        """
        Validate a recovery code and reset user password.
        Returns True if successful, False if code is invalid.
        """
        try:
            recovery_code = RecoveryCode.objects.get(code=code)
            user = recovery_code.user
            user.set_password(new_password)
            user.save()
            
            # Delete the used code
            recovery_code.delete()
            return True
        except RecoveryCode.DoesNotExist:
            return False
