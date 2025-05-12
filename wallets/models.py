from django.db import models

from mobile_bankings.models import Fee
from users.models import CustomUser

# Create your models here.

class Transaction(models.Model):
    """Transaction records for deposits and withdrawals"""
    FROM_TYPE_CHOICES = [
        ('wallet', 'Wallet'),
        ('card', 'Card'),
    ]
    
    TO_TYPE_CHOICES = [
        ('wallet', 'Wallet'),
        ('mobile', 'Mobile'),
    ]
    
    TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    from_type = models.CharField(max_length=10, choices=FROM_TYPE_CHOICES)
    from_id = models.IntegerField()
    to_type = models.CharField(max_length=10, choices=TO_TYPE_CHOICES)
    to_id = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.ForeignKey(Fee, on_delete=models.PROTECT)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} - {self.timestamp}"

