from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# Club Model
# -----------------------------
class Club(models.Model):
    club_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_clubs")

    def __str__(self):
        return self.name


# -----------------------------
# Event Model
# -----------------------------
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    location = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")

    def __str__(self):
        return self.title


# -----------------------------
# Post Model
# -----------------------------
class Post(models.Model):
    id_post = models.AutoField(primary_key=True)
    content = models.TextField()
    image_url = models.URLField(max_length=255, blank=True, null=True)
    date_post = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"Post {self.id_post} by {self.user}"


# -----------------------------
# Notification Model
# -----------------------------
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    message = models.TextField()
    sent_date = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # ✅ ADD THIS
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="notifications")


# -----------------------------
# User_Club (Many-to-Many)
# -----------------------------
class UserClub(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)  # ✅ ADD THIS LINE

    class Meta:
        unique_together = ('user', 'club')

    def __str__(self):
        return f"{self.user} in {self.club}"


# -----------------------------
# MembershipRequest Model
# -----------------------------
class MembershipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="membership_requests")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="membership_requests")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    reviewed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'club')

    def __str__(self):
        return f"{self.user.username} -> {self.club.name} ({self.status})"

# -----------------------------
# ClubMessage Model
# -----------------------------
class ClubMessage(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.club.name}: {self.content[:30]}"