from django.shortcuts import render
from banks.models import CardAccount
from mobile_bankings.models import Fee, MobileAccount
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db import transaction
from decimal import Decimal

from users.models import SystemAccount
from wallets.serializers import DepositSerializer, TransactionSerializer, WithdrawSerializer
from wallets.models import Transaction


User = get_user_model()

# Create your views here.
class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def deposit(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        card_id = serializer.validated_data['card_id']
        amount = serializer.validated_data['amount']
        
        try:
            # Verify card ownership
            card = CardAccount.objects.get(id=card_id, user=request.user)
            
            # Get fee
            fee = Fee.objects.get(method_type='deposit', payment_type='card')
            fee_amount = fee.calculate_fee(amount)
            total_amount = amount - fee_amount  # Fee deducted from deposit
            
            with transaction.atomic():
                # Create transaction record
                trans = Transaction.objects.create(
                    user=request.user,
                    from_type='card',
                    from_id=card.id,
                    to_type='wallet',
                    to_id=request.user.wallet.id,
                    type='deposit',
                    amount=amount,
                    fee=fee,
                    fee_amount=fee_amount
                )
                
                # Update wallet balance
                wallet = SystemAccount.objects.select_for_update().get(user=request.user)
                wallet.balance += total_amount
                wallet.save()
                
                return Response({
                    'message': 'Deposit successful',
                    'transaction_id': trans.id,
                    'amount': amount,
                    'fee': fee_amount,
                    'credited': total_amount,
                    'new_balance': wallet.balance
                }, status=status.HTTP_201_CREATED)
                
        except CardAccount.DoesNotExist:
            return Response(
                {"error": "Card not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def withdraw(self, request):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        mobile_id = serializer.validated_data['mobile_id']
        amount = serializer.validated_data['amount']
        
        try:
            # Verify mobile account ownership
            mobile = MobileAccount.objects.get(id=mobile_id, user=request.user)
            
            # Get fee
            fee = Fee.objects.get(method_type='withdraw', payment_type=mobile.type)
            fee_amount = fee.calculate_fee(amount)
            total_debit = amount + fee_amount  # Fee added to withdrawal
            
            with transaction.atomic():
                # Check wallet balance
                wallet = SystemAccount.objects.select_for_update().get(user=request.user)
                
                if wallet.balance < total_debit:
                    return Response(
                        {"error": "Insufficient balance"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create transaction record
                trans = Transaction.objects.create(
                    user=request.user,
                    from_type='wallet',
                    from_id=wallet.id,
                    to_type='mobile',
                    to_id=mobile.id,
                    type='withdraw',
                    amount=amount,
                    fee=fee,
                    fee_amount=fee_amount
                )
                
                # Update wallet balance
                wallet.balance -= total_debit
                wallet.save()
                
                # TODO: Trigger payment gateway API call here
                # payment_gateway.process_withdrawal(mobile, amount)
                
                return Response({
                    'message': 'Withdrawal successful',
                    'transaction_id': trans.id,
                    'amount': amount,
                    'fee': fee_amount,
                    'total_debited': total_debit,
                    'new_balance': wallet.balance
                }, status=status.HTTP_201_CREATED)
                
        except MobileAccount.DoesNotExist:
            return Response(
                {"error": "Mobile account not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
