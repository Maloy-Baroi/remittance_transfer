from django.shortcuts import render
from banks.models import CardAccount
from banks.serializers import CardAccountSerializer
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from decimal import Decimal

from users.models import SystemAccount
from users.serializers import SystemAccountSerializer

# Create your views here.
User = get_user_model()

class WalletView(generics.RetrieveAPIView):
    serializer_class = SystemAccountSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return SystemAccount.objects.get(user=self.request.user)


class CardAccountViewSet(viewsets.ModelViewSet):
    serializer_class = CardAccountSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CardAccount.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        # Prevent deletion as per requirements
        return Response(
            {"error": "Card accounts cannot be deleted"},
            status=status.HTTP_403_FORBIDDEN
        )


