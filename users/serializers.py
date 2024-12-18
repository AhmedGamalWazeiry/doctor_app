from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        ref_name = None

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],)
        return user


class AddUser(serializers.ModelSerializer):
    can_deleted = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',)
        extra_kwargs = {'password': {'write_only': True}}
        ref_name = None

    def create(self, validated_data):

        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],
                                        email=validated_data['email'],
                                        )
        return user