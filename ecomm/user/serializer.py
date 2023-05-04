from .models import UserBase
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class Registration(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        user = UserBase.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = UserBase
        fields = ('email', 'username', 'password',
                  'password_confirmation')
