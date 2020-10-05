from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.utils.text import gettext_lazy


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=155)
    last_name = serializers.CharField(max_length=155)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid Credentials, Please enter valid details.')
        if not user.is_active:
            raise AuthenticationFailed('Your account is inactive, Please contact admin.')
        return {
            'email': user.email,
            'password': user.password,
            'tokens': user.tokens()
        }

        return super().validate(attrs)


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']


class PasswordResetTokenCheckSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, write_only=True)
    uidb4 = serializers.CharField(max_length=58, write_only=True)

    class Meta:
        model = User
        fields = ['token', 'uidb4']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb4 = attrs.get('uidb4')
        except Exception as error:
            raise AuthenticationFailed({'error': error})


class SetNewPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=58, min_length=6, write_only=True)
    token = serializers.CharField(max_length=255, write_only=True)
    uidb4 = serializers.CharField(max_length=58, write_only=True)

    class Meta:
        model = User
        fields = ['new_password', 'token', 'uidb4']

    def validate(self, attrs):
        try:
            new_password = attrs.get('new_password')
            token = attrs.get('token')
            uidb4 = attrs.get('uidb4')
            id = force_str(urlsafe_base64_decode(uidb4))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid')
            user.set_password(new_password)
            user.save()
            return user
        except Exception as error:
            raise AuthenticationFailed({'error': error})
        return super().validate(attrs)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': gettext_lazy('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')