from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('email_verification/<uidb4>/<token>/', EmailVerification.as_view(), name='email_verification'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset_request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset_token_check/<uidb4>/<token>/', PasswordResetTokenCheckView.as_view(),
         name='password_reset_token_check'),
    path('set_new_password/', SetNewPasswordView.as_view(), name='set_new_password'),
]
