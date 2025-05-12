from rest_framework import serializers
from .models import (
    MobileAccount, Fee
)

class MobileAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileAccount
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class FeeSerializer(serializers.ModelSerializer):
    total_fee = serializers.SerializerMethodField()
    
    class Meta:
        model = Fee
        fields = '__all__'
    
    def get_total_fee(self, obj):
        # Example calculation for display purposes
        amount = self.context.get('amount', 100)
        return obj.calculate_fee(amount)