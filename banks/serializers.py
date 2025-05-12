from rest_framework import serializers
from .models import CardAccount


class CardAccountSerializer(serializers.ModelSerializer):
    display_number = serializers.SerializerMethodField()
    
    class Meta:
        model = CardAccount
        fields = ['id', 'number', 'card_name', 'expiry_date', 'secret_no', 
                  'display_number', 'created_at', 'updated_at']
        extra_kwargs = {
            'number': {'write_only': True},
            'secret_no': {'write_only': True}
        }
    
    def get_display_number(self, obj):
        return f"****{obj.number[-4:]}"
    
    def validate_number(self, value):
        # Store only last 4 digits for security
        return value[-4:]
