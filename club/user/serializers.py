from rest_framework import serializers
from .models import User, Club, Event, Post, Notification, UserClub

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
