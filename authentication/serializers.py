from rest_framework import serializers
from django.contrib.auth import authenticate
from datetime import datetime, timedelta

from .models import User, Account
from fly_image_python.settings import JWT_TOKEN_LIFETIME_MIN

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)

        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'telegramm', 'user']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data.get('user'))
        return Account.objects.create_account(user=user,
                                              first_name=validated_data.get('first_name',''),
                                              last_name=validated_data.get('last_name',''),
                                              telegramm=validated_data.get('telegramm', ''))


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    creation = serializers.IntegerField(read_only=True)
    expiration = serializers.IntegerField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'token': user.token,
            'creation':datetime.now().timestamp()*1000,
            'expiration':(datetime.now() + timedelta(minutes=JWT_TOKEN_LIFETIME_MIN)).timestamp()*1000
        }
        