from decimal import Decimal
from django.db import models

from users.models import CustomUser

# Create your models here.
class MobileAccount(models.Model):
    """Mobile money accounts (bKash/Nagad)"""
    PROVIDER_CHOICES = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
    ]
    
    ACCOUNT_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('agent', 'Agent'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mobile_accounts')
    type = models.CharField(max_length=10, choices=PROVIDER_CHOICES)
    phone_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=255)
    address = models.TextField()
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.phone_number}"


class Fee(models.Model):
    """Fee structure for transactions"""
    METHOD_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('card', 'Card'),
    ]
    
    method_type = models.CharField(max_length=10, choices=METHOD_CHOICES)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    flat_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    class Meta:
        unique_together = ['method_type', 'payment_type']
    
    def calculate_fee(self, amount):
        """Calculate total fee for a given amount"""
        percentage_fee = (amount * self.percentage) / 100
        return percentage_fee + self.flat_fee
