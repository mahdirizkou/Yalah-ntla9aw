from rest_framework import serializers
from .models import User, Club, Event, Post, Notification, UserClub
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = 'email'

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                "No active account found with the given credentials"
            )

    
        attrs['username'] = email

 
        data = super().validate(attrs)

       
        data.update({
            'user': {
                'id_user': user.id_user,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'type': user.type,
            }
        })

        return data
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'first_name', 'last_name', 'email', 'password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
# -----------------------------
# User Serializer
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# -----------------------------
# Club Serializer
# -----------------------------
class ClubSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)  

    class Meta:
        model = Club
        fields = '__all__'


# -----------------------------
# Event Serializer
# -----------------------------
class EventSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


# -----------------------------
# Post Serializer
# -----------------------------
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


# -----------------------------
# Notification Serializer
# -----------------------------
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'


# -----------------------------
# UserClub Serializer
# -----------------------------
class UserClubSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = UserClub
        fields = '__all__'
