from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import BaseUser, Contact, ContactType


class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = ['id', 'name']


class ContactSerializer(serializers.ModelSerializer):
    type = ContactTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=ContactType.objects.all(), source='type', write_only=True
    )

    class Meta:
        model = Contact
        fields = ['id', 'owner', 'type', 'type_id', 'value']
        # No authentication on these endpoints yet, so the client sends "owner".
        # Later: add read_only_fields = ['owner'] and use serializer.save(owner=request.user)


class BaseUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True, required=False, style={'input_type': 'password'}
    )
    # Read-only: contacts are created/updated/deleted through /api/contacts/
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = BaseUser
        fields = [
            'id', 'username', 'email', 'password', 'confirm_password',
            'first_name', 'last_name', 'profile', 'contacts',
            'date_joined', 'is_active',
        ]
        read_only_fields = ['date_joined', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password', None)

        # Only check passwords when one was actually sent (POST, or PATCH changing it)
        if password is not None or confirm_password is not None:
            if password != confirm_password:
                raise serializers.ValidationError({
                    'confirm_password': 'Password and Confirm Password do not match!'
                })
            try:
                validate_password(password, user=self.instance)  # type: ignore
            except DjangoValidationError as error:
                raise serializers.ValidationError({'password': error.messages}) from error

        return attrs

    def create(self, validated_data):
        return BaseUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=attrs['password'],
        )
        if user is None:  # also None for inactive (soft-deleted) users
            raise serializers.ValidationError({'detail': 'Invalid username or password.'})

        attrs['user'] = user
        return attrs
