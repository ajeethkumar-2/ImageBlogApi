from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError, smart_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import (
    PasswordResetTokenCheckSerializer,
    SetNewPasswordSerializer,
    PasswordResetSerializer,
    RefreshTokenSerializer,
    SignupSerializer,
    LoginSerializer,
)
from rest_framework import status
from .models import User
from .utils import Util


class SignupAPIView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.data['email']
        first_name = serializer.data['first_name']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb4 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('email_verification', kwargs={'uidb4': uidb4, 'token': token})
            absolute_url = 'http://' + current_site + relativeLink
            email_body = 'Hello, ' + first_name + '\n\nUse the link verify your email id ' \
                                                  'and to complete the registration\n\n' + absolute_url
            data = {'email_subject': 'Verify your email id', 'email_body': email_body, 'to_email': user.email}
            Util.send_email(data)

            return Response({
                'message': 'New user created SuccessFully. '
                           'Check your mail and verify your email id to complete the registration',
                'data': serializer.data,
                'uidb4': uidb4,
                'token': token,

            }, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(GenericAPIView):
    serializer_class = PasswordResetTokenCheckSerializer

    def get(self, request, uidb4, token):
        try:
            id = urlsafe_base64_decode(uidb4)
            user = User.objects.get(id=id)
            verification = PasswordResetTokenGenerator()
            if verification.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({'message': 'Congratulations, Your email id had verified, You can login Now.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Verification - Token is not valid, Please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is not valid, Please request a new one'},

                            status=status.HTTP_401_UNAUTHORIZED)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if serializer.is_valid(raise_exception=True):
            if User.objects.filter(email=email).exists():
                return Response({'message': 'Login Successful.', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No account is linked with this email. Check again please.'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': serializer.default_error_messages}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb4 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password_reset_token_check', kwargs={'uidb4': uidb4, 'token': token})
            absolute_url = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n Use the link below to reset your password. \n' + absolute_url
            data = {'email_subject': 'Reset your Password', 'email_body': email_body, 'to_email': user.email}
            Util.send_email(data)

        return Response({'success': 'We have sent you the link to reset your password..!!',
                         'email': data}, status=status.HTTP_200_OK)


class PasswordResetTokenCheckView(GenericAPIView):

    def get(self, request, uidb4, token):
        try:
            id = urlsafe_base64_decode(smart_str(uidb4))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, Please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials is Valid', 'uidb4': uidb4, 'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as error:
            return Response({'error': 'Token is not valid, Please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password Reset Success..!!'}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args):
        logout = self.get_serializer(data=request.data)
        logout.is_valid(raise_exception=True)
        logout.save()
        return Response({'success': True, 'message': 'You Have Logged Out..!!'}, status=status.HTTP_204_NO_CONTENT)
