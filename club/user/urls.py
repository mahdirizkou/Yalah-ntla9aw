from django.urls import path
from .views import (
    UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView,
    ClubListCreateAPIView, ClubRetrieveUpdateDestroyAPIView,
    EventListCreateAPIView, EventRetrieveUpdateDestroyAPIView,
    PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView,
    NotificationListCreateAPIView, NotificationRetrieveUpdateDestroyAPIView,
    UserClubListCreateAPIView, UserClubRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # User
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:id_user>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    # Club
    path('clubs/', ClubListCreateAPIView.as_view(), name='club-list-create'),
    path('clubs/<int:club_id>/', ClubRetrieveUpdateDestroyAPIView.as_view(), name='club-detail'),

    # Event
    path('events/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('events/<int:event_id>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-detail'),

    # Post
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:id_post>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),

    # Notification
    path('notifications/', NotificationListCreateAPIView.as_view(), name='notification-list-create'),
    path('notifications/<int:notification_id>/', NotificationRetrieveUpdateDestroyAPIView.as_view(), name='notification-detail'),

    # UserClub
    path('userclubs/', UserClubListCreateAPIView.as_view(), name='userclub-list-create'),
    path('userclubs/<int:id>/', UserClubRetrieveUpdateDestroyAPIView.as_view(), name='userclub-detail'),
]
