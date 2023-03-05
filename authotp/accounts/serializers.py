from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname', 'password', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class VerifyAccountSerializer(serializers.Serializer):
    otpemail = serializers.CharField()
    otp = serializers.CharField()


class LogInSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()







      

