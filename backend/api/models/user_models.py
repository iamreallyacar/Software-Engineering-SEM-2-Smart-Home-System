from django.db import models
from django.contrib.auth.models import User
import random
import string


class UserProfile(models.Model):
    """
    Extends the built-in User model with additional profile information.
    
    This gives us a place to store user details that aren't covered by
    Django's default User model, like date of birth and contact information.
    
    The one-to-one relationship ensures each user has exactly one profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, default=None)
    gender = models.CharField(
        max_length=10, 
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], 
        null=True,
        default=None
    )
    phone_number = models.CharField(max_length=15, null=True, default=None)
    
    def __str__(self):
        return f"Profile for {self.user.username}"


class RecoveryCode(models.Model):
    """
    One-time use codes that let users recover their account if they forget their password.
    
    Each user can have up to 10 recovery codes. When a user uses a code to reset their
    password, that code is deleted so it can't be used again. The codes follow a specific
    format (xxxxx-xxxxx) to make them easy to read and enter.
    
    Recovery codes are a security best practice, providing an alternative to email-based
    password reset which may not always be accessible.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recovery_codes')
    code = models.CharField(max_length=12, unique=True)  # Format: xxxxx-xxxxx
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Recovery code for {self.user.username}"
    
    @classmethod
    def generate_code(cls):
        """
        Creates a new random recovery code in the format xxxxx-xxxxx.
        
        We use a mix of lowercase letters and digits to make codes
        that are secure but still readable.
        """
        chars = string.ascii_lowercase + string.digits
        part1 = ''.join(random.choices(chars, k=5))
        part2 = ''.join(random.choices(chars, k=5))
        return f"{part1}-{part2}"
    
    @classmethod
    def create_for_user(cls, user, count=10):
        """
        Creates a fresh set of recovery codes for a user.
        
        This removes any existing codes the user has (for security),
        then generates a new set of unique codes. By default, we create
        10 codes, giving users plenty of recovery options while keeping
        the number manageable.
        """
        # First, invalidate any existing unused codes
        cls.objects.filter(user=user).delete()
        
        # Generate new codes
        new_codes = []
        for _ in range(count):
            code = cls.generate_code()
            while cls.objects.filter(code=code).exists():
                code = cls.generate_code()  # Ensure uniqueness
                
            new_code = cls.objects.create(user=user, code=code)
            new_codes.append(new_code)
            
        return new_codes
