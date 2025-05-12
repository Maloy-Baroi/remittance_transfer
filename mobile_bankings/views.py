from mobile_bankings.models import Fee, MobileAccount
from mobile_bankings.serializers import FeeSerializer, MobileAccountSerializer
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

# Create your views here.
class MobileAccountViewSet(viewsets.ModelViewSet):
    serializer_class = MobileAccountSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MobileAccount.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        # Prevent deletion as per requirements
        return Response(
            {"error": "Mobile accounts cannot be deleted"},
            status=status.HTTP_403_FORBIDDEN
        )


class FeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    permission_classes = [IsAuthenticated]
