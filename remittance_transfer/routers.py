# remittance_app/urls.py
from django.urls import path, include
from banks.views import CardAccountViewSet, WalletView
from mobile_bankings.views import FeeViewSet, MobileAccountViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomTokenObtainPairView, SystemProfileViewSet, UserDetailView, UserRegistrationView
from wallets.views import TransactionViewSet

router = DefaultRouter()
router.register('profiles', SystemProfileViewSet, basename='profile')
router.register('cards', CardAccountViewSet, basename='card')
router.register('mobiles', MobileAccountViewSet, basename='mobile')
router.register('fees', FeeViewSet, basename='fee')
router.register('transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    # Authentication
    path('auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User
    path('users/me/', UserDetailView.as_view(), name='user_detail'),
    
    # Wallet
    path('wallets/me/', WalletView.as_view(), name='wallet_detail'),
    
    # Router URLs
    path('', include(router.urls)),
]