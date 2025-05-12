from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from decimal import Decimal
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email as unique identifier"""
    email = models.EmailField(unique=True)
    bangladeshi_passport_no = models.CharField(max_length=15)
    passport_photo = models.ImageField(upload_to="/user_photo/")
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['bangladeshi_passport_no', 'password']
    
    def __str__(self):
        return self.email


class SystemProfile(models.Model):
    """User profile information for remittance system"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    current_country = models.CharField(max_length=100)
    bd_phone = models.CharField(max_length=20)
    bd_address = models.TextField()
    last_travel_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.email}"


class SystemAccount(models.Model):
    """System wallet for user"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - Balance: {self.balance}"
