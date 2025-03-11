from rest_framework import serializers
from .models import CustomUser
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', "email", 'first_name', 'last_name', 'phone_number', 'password')

    def validate_phone_number(self, value):
        pattern = re.compile(r'^(\+380\d{9}|0\d{9})$')
        if not pattern.match(value):
            raise serializers.ValidationError("Invalid phone number format. Must be +380XXXXXXXXX or 0XXXXXXXXX.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()
        return instance
