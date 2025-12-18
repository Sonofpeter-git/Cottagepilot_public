from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from django.core.exceptions import ValidationError as DjangoValidationError

class UserSerializer(serializers.ModelSerializer):
    cottage_plan = serializers.CharField(source='access_to_cottage.stripe_subscription', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_color', 'access_to_cottage', 'cottage_plan']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username').lower()  # Normalize to lowercase
        user = authenticate(username=username, password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        data['user'] = user
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'A user with that username already exists.'})
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'A user with that email already exists.'})
        
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password2': "Passwords do not match."})

        try:
            validate_password(data['password1'], user=None)
        except DjangoValidationError as e:
            # Map Django's password validation errors to password1 field
            raise serializers.ValidationError({'password1': list(e.messages)})

        return data

    def create(self, validated_data):

        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.is_active = False
        user.set_password(validated_data['password1'])
        user.save()
        return user

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
