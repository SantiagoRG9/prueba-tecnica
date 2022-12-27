from rest_framework import serializers
from app.user.models import User


#  -------------------------- SERIALIZADORES DE USUARIOS -----------------------------

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','name','last_name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions') # SE EXCLUYE (groups y permission) PARA EVITAR ALGUN PROBLEMA CON EL REGISTRO

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email', 'name', 'last_name')


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password' : 'Debe ingresar ambas contraseñas iguales'
                })
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id' : instance['id'],
            'username' : instance['username'],
            'email':instance['email'],
            'name' : instance['name'],
        }