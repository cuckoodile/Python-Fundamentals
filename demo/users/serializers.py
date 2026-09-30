from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User

# Syntax:
# class {Model}Serializer
class UserSerializer(serializers.ModelSerializer):
    c_pass = serializers.CharField()

    # 1. Data representation
    # Serializing = Python => JSON (Get)
    #  and 
    # Deserializing = JSON => Python (Write)

    # 2. Formatting (Fields representation)
    class Meta:
        model = User
        # fields = ['__all__']
        fields = [
            'id', 
            'username', 
            'email', 
            'password', # Write only field (Create or Update)
            'c_pass',
            'date_joined', 
            'avatar', 
            'first_name', 
            'last_name',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
        }

    def validate_password(self, data):
        return validate_password(data.password)

    def create(self, data):
        """
        data = {
            "id": 2,
            "username": "cuckoodile",
            "email": "",
            "password": "Password123!",
            "date_joined": "2026-09-09T15:40:30.154699+08:00",
            "avatar": "/media/avatar/default.webp",
            "first_name": "",
            "last_name": ""
        }
        """

        password = data.pop('password', None)
        c_pass = data.pop('c_pass', None)
        # 1. get attribue value
        # 2. return the retrieved value
        # 3. remove the retrieved value from the original dictionary (data)

        if password != c_pass:
            return serializers.ValidationError({"detail": "Password and Confirm Password does not match!"})

        user = User(**data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        # Parameter vs Argument
        # Param: Inside a function during definition.
        # Argu: Value passed when the function is called.

        """ JSON (PATCH)
        {
            "first_name": "ian",
            "last_name": "sube"
        }
        """

        # Save the validated instance
        # return the instance