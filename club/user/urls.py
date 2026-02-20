from django.urls import path
from .views.apiviews import (
    UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView,
    ClubListCreateAPIView, ClubRetrieveUpdateDestroyAPIView,
    EventListCreateAPIView, EventRetrieveUpdateDestroyAPIView,
    PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView,
    NotificationListCreateAPIView, NotificationRetrieveUpdateDestroyAPIView,
    UserClubListCreateAPIView, UserClubRetrieveUpdateDestroyAPIView,
    RegisterView, LoginView,
    MembershipRequestListCreateAPIView,
    MyMembershipRequestsAPIView,
    MembershipRequestDetailAPIView,
    ClubMembershipRequestsAPIView,
    MembershipRequestRespondAPIView,
    ClubMembersAPIView, ClubMessagesAPIView, NotificationMarkReadAPIView # ✅ Make sure this is imported
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # User
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:id_user>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    # Club
    path('clubs/', ClubListCreateAPIView.as_view(), name='club-list-create'),
    path('clubs/<int:club_id>/', ClubRetrieveUpdateDestroyAPIView.as_view(), name='club-detail'),
    path('clubs/<int:club_id>/requests/', ClubMembershipRequestsAPIView.as_view(), name='club-requests'),
    path('clubs/<int:club_id>/members/', ClubMembersAPIView.as_view(), name='club-members'),  # ✅ This line must exist

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

    # Membership Requests
    path('membership-requests/', MembershipRequestListCreateAPIView.as_view(), name='membership-request-list-create'),
    path('my-membership-requests/', MyMembershipRequestsAPIView.as_view(), name='my-membership-requests'),
    path('membership-requests/<int:id>/', MembershipRequestDetailAPIView.as_view(), name='membership-request-detail'),
    path('membership-requests/<int:request_id>/respond/', MembershipRequestRespondAPIView.as_view(), name='membership-request-respond'),

# Membership Requests
    path('clubs/<int:club_id>/messages/', ClubMessagesAPIView.as_view(), name='club-messages'),

    path('notifications/<int:notification_id>/read/', NotificationMarkReadAPIView.as_view(), name='notification-mark-read'),
]