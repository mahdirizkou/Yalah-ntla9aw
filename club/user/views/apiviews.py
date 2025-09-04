from rest_framework import generics
from rest_framework.views import APIView
from ..models import Club, Event, Post, Notification, UserClub
from django.contrib.auth.hashers import check_password
from ..serializers import (
    ClubSerializer, EventSerializer,
    PostSerializer, NotificationSerializer, UserClubSerializer 
)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer
from rest_framework_simplejwt.exceptions import TokenError



# -----------------------------
# Token
# -----------------------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        tokens = get_tokens_for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "tokens": tokens,
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "tokens": tokens,
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
# -----------------------------
# User API Views classic methode
# -----------------------------
# class UserListCreateAPIView(APIView):
#     def get(self,request):
#         u = User.objects.all()
#         s = UserSerializer(u ,many = True)
#         return Response(s.data)
    
#     def post(self,request):
#         s=UserSerializer(data= request.data)    
#         if s.is_valid():
#             s.save()
#             return Response(s.data, status = status.HTTP_201_CREATED)
#         return Response(s.errors, status = status.HTTP_400_BAD_REQUEST)
# -----------------------------
# User API Views generic methode
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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ClubRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    lookup_field = 'club_id'
    permission_classes = [IsAuthenticated]


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
