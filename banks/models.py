from django.db import models

from users.models import CustomUser

# Create your models here.
class CardAccount(models.Model):
    """Card accounts linked to user"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='card_accounts')
    number = models.CharField(max_length=16)  # Last 4 digits only for security
    card_name = models.CharField(max_length=255)
    expiry_date = models.CharField(max_length=7)  # MM/YYYY format
    secret_no = models.CharField(max_length=3)  # CVV - should be encrypted in production
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.card_name} - ****{self.number[-4:]}"

