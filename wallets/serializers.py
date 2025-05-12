from mobile_bankings.serializers import FeeSerializer
from rest_framework import serializers
from .models import (Transaction
)

class TransactionSerializer(serializers.ModelSerializer):
    fee_details = FeeSerializer(source='fee', read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'fee_amount', 'timestamp']


class DepositSerializer(serializers.Serializer):
    card_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value


class WithdrawSerializer(serializers.Serializer):
    mobile_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value