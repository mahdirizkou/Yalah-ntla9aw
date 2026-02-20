from rest_framework import serializers
from .models import Club, Event, Post, Notification, UserClub ,MembershipRequest,ClubMessage
from django.contrib.auth.models import User


# -----------------------------
# User Serializer
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


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
    club_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Event
        fields = '__all__'

    def validate_club_id(self, value):
        if not Club.objects.filter(club_id=value).exists():
            raise serializers.ValidationError("Club not found")
        return value

    def create(self, validated_data):
        club_id = validated_data.pop("club_id")
        club = Club.objects.get(club_id=club_id)
        return Event.objects.create(club=club, **validated_data)


# -----------------------------
# Post Serializer
# -----------------------------
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)
    club_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Post
        fields = ["id_post", "content", "image_url", "date_post", "user", "club", "club_id"]
        read_only_fields = ["id_post", "date_post", "user", "club"]

    def validate_club_id(self, value):
        if not Club.objects.filter(club_id=value).exists():
            raise serializers.ValidationError("Club not found")
        return value

    def create(self, validated_data):
        club_id = validated_data.pop("club_id")
        club = Club.objects.get(club_id=club_id)
        user = validated_data.pop("user", None)
        return Post.objects.create(user=user, club=club, **validated_data)


# -----------------------------
# Notification Serializer
# -----------------------------
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)
    club_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Notification
        fields = '__all__'  # is_read will be included automatically

# -----------------------------
# UserClub Serializer
# -----------------------------
class UserClubSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)
    club_id = serializers.IntegerField(write_only=True, required=False)
    user_id = serializers.IntegerField(write_only=True, required=False)
    # ✅ REMOVE the line: date_joined = serializers.DateTimeField(read_only=True, source='id')
    # date_joined will now come from the model automatically

    class Meta:
        model = UserClub
        fields = '__all__'

    def validate_club_id(self, value):
        if not Club.objects.filter(club_id=value).exists():
            raise serializers.ValidationError("Club not found")
        return value

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found")
        return value

    def create(self, validated_data):
        club_id = validated_data.pop("club_id", None)
        user_id = validated_data.pop("user_id", None)
        
        if club_id:
            club = Club.objects.get(club_id=club_id)
        else:
            club = validated_data.get('club')
            
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            user = validated_data.get('user')
            
        return UserClub.objects.create(user=user, club=club, **validated_data)

        # -----------------------------
# MembershipRequest Serializer
# -----------------------------
class MembershipRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)
    club_id = serializers.IntegerField(write_only=True, required=False)
    request_id = serializers.IntegerField(source='id', read_only=True)  # ADD THIS LINE

    class Meta:
        model = MembershipRequest
        fields = ['request_id', 'user', 'club', 'club_id', 'status', 'request_date', 'reviewed_date']
        read_only_fields = ['request_id', 'user', 'club', 'status', 'request_date', 'reviewed_date']

    def validate_club_id(self, value):
        if not Club.objects.filter(club_id=value).exists():
            raise serializers.ValidationError("Club not found")
        return value

    def create(self, validated_data):
        club_id = validated_data.pop("club_id")
        club = Club.objects.get(club_id=club_id)
        user = validated_data.pop("user", None)
        
        # Check if user is already a member
        if UserClub.objects.filter(user=user, club=club).exists():
            raise serializers.ValidationError("You are already a member of this club")
        
        # Check if request already exists
        if MembershipRequest.objects.filter(user=user, club=club, status='pending').exists():
            raise serializers.ValidationError("You already have a pending request for this club")
        
        return MembershipRequest.objects.create(user=user, club=club, **validated_data)

    # -----------------------------
# ClubMessage Serializer
# -----------------------------
class ClubMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ClubMessage
        fields = ['id', 'content', 'sender', 'club', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']