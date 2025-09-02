from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from ..models import User, Club, Event, Post, Notification, UserClub
from rest_framework.response import Response
from ..serializers import (
    UserSerializer, ClubSerializer, EventSerializer,
    PostSerializer, NotificationSerializer, UserClubSerializer,
    RegisterSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView


# -----------------------------
# Register
# -----------------------------
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# Login (JWT)
# -----------------------------
class LoginAPIView(TokenObtainPairView):
    """
   
    """
    pass


# -----------------------------
# User API Views generic method
# -----------------------------
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id_user'

# -----------------------------
# Club API Views
# -----------------------------
class ClubListCreateAPIView(generics.ListCreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

class ClubRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    lookup_field = 'club_id'


# -----------------------------
# Event API Views
# -----------------------------
class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'event_id'


# -----------------------------
# Post API Views
# -----------------------------
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id_post'


# -----------------------------
# Notification API Views
# -----------------------------
class NotificationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = 'notification_id'


# -----------------------------
# UserClub API Views
# -----------------------------
class UserClubListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserClub.objects.all()
    serializer_class = UserClubSerializer

class UserClubRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserClub.objects.all()
    serializer_class = UserClubSerializer
    lookup_field = 'id'  
