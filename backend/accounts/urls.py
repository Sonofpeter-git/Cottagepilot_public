from django.urls import path, include
from .views import AccountViewSet, CustomObtainAuthToken, csrf, signup, RequestPasswordResetView, PasswordResetConfirmView, SetNewPasswordView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'account', AccountViewSet, basename='account')


urlpatterns = [
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('signup/', signup, name='login'),
    path('csrf/', csrf, name='get_csrf'),
    path('', include(router.urls)),
    path('password-reset/', RequestPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/complete/', SetNewPasswordView.as_view(), name='password-reset-complete'),
]
