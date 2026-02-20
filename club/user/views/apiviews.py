from rest_framework import generics
from rest_framework.views import APIView
from ..models import Club, Event, Post, Notification, UserClub, MembershipRequest, ClubMessage
from ..serializers import (
    ClubSerializer, EventSerializer, PostSerializer,
    NotificationSerializer, UserClubSerializer,
    MembershipRequestSerializer, ClubMessageSerializer
)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer
from django.utils import timezone


# -----------------------------
# Token
# -----------------------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# -----------------------------
# Register & Login
# -----------------------------
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if email and User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
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
# User API Views
# -----------------------------
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id_user'


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
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
    permission_classes = [IsAuthenticated]


class NotificationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = 'notification_id'


# -----------------------------
# Notification Mark as Read
# -----------------------------
class NotificationMarkReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        try:
            notif = Notification.objects.get(
                notification_id=notification_id,
                user=request.user
            )
            notif.is_read = True
            notif.save(update_fields=['is_read'])
            return Response({"message": "Marked as read"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# -----------------------------
# UserClub API Views
# -----------------------------
class UserClubListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserClub.objects.all()
    serializer_class = UserClubSerializer
    permission_classes = [IsAuthenticated]


class UserClubRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserClub.objects.all()
    serializer_class = UserClubSerializer
    lookup_field = 'id'


# -----------------------------
# MembershipRequest API Views
# -----------------------------
class MembershipRequestListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MembershipRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MembershipRequest.objects.filter(club__creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyMembershipRequestsAPIView(generics.ListAPIView):
    serializer_class = MembershipRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MembershipRequest.objects.filter(user=self.request.user)


class MembershipRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MembershipRequest.objects.all()
    serializer_class = MembershipRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'approved':
            UserClub.objects.get_or_create(user=instance.user, club=instance.club)
            instance.reviewed_date = timezone.now()
            instance.save()


class ClubMembershipRequestsAPIView(generics.ListAPIView):
    serializer_class = MembershipRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        club_id = self.kwargs.get('club_id')
        return MembershipRequest.objects.filter(
            club__club_id=club_id,
            club__creator=self.request.user,
            status='pending'
        ).select_related('user', 'club', 'club__creator')


class MembershipRequestRespondAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, request_id):
        try:
            membership_request = MembershipRequest.objects.select_related(
                'user', 'club', 'club__creator'
            ).get(id=request_id)

            if membership_request.club.creator != request.user:
                return Response(
                    {"error": "Only club creator can respond to requests"},
                    status=status.HTTP_403_FORBIDDEN
                )

            action = request.data.get('action')

            if action == 'accept':
                UserClub.objects.get_or_create(
                    user=membership_request.user,
                    club=membership_request.club
                )
                membership_request.status = 'approved'
                membership_request.reviewed_date = timezone.now()
                membership_request.save()

                try:
                    Notification.objects.get_or_create(
                        user=membership_request.user,
                        club=membership_request.club,
                        message=f"Your request to join {membership_request.club.name} has been accepted!",
                        defaults={'is_read': False}
                    )
                except Exception as e:
                    print(f"Notification creation failed: {e}")

                return Response(
                    {"message": "Request accepted successfully"},
                    status=status.HTTP_200_OK
                )

            elif action == 'reject':
                membership_request.status = 'rejected'
                membership_request.reviewed_date = timezone.now()
                membership_request.save()

                try:
                    Notification.objects.get_or_create(
                        user=membership_request.user,
                        club=membership_request.club,
                        message=f"Your request to join {membership_request.club.name} has been rejected.",
                        defaults={'is_read': False}
                    )
                except Exception as e:
                    print(f"Notification creation failed: {e}")

                return Response(
                    {"message": "Request rejected successfully"},
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {"error": "Invalid action. Use 'accept' or 'reject'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except MembershipRequest.DoesNotExist:
            return Response(
                {"error": "Request not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# -----------------------------
# Club Members View
# -----------------------------
class ClubMembersAPIView(generics.ListAPIView):
    """Get all members of a specific club"""
    serializer_class = UserClubSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        club_id = self.kwargs.get('club_id')
        return UserClub.objects.filter(club__club_id=club_id).select_related('user', 'club')


# -----------------------------
# Club Messages API View
# -----------------------------
class ClubMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, club_id):
        club = Club.objects.filter(club_id=club_id).first()
        if not club:
            return Response({"error": "Club not found"}, status=status.HTTP_404_NOT_FOUND)

        is_member = UserClub.objects.filter(user=request.user, club=club).exists()
        is_creator = club.creator == request.user

        if not is_member and not is_creator:
            return Response({"error": "You are not a member of this club"}, status=status.HTTP_403_FORBIDDEN)

        messages = ClubMessage.objects.filter(club=club).select_related('sender')
        serializer = ClubMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, club_id):
        club = Club.objects.filter(club_id=club_id).first()
        if not club:
            return Response({"error": "Club not found"}, status=status.HTTP_404_NOT_FOUND)

        is_member = UserClub.objects.filter(user=request.user, club=club).exists()
        is_creator = club.creator == request.user

        if not is_member and not is_creator:
            return Response({"error": "You are not a member of this club"}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content', '').strip()
        if not content:
            return Response({"error": "Message content cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        message = ClubMessage.objects.create(
            content=content,
            sender=request.user,
            club=club
        )
        serializer = ClubMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)