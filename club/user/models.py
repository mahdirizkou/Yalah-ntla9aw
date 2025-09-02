from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
# -----------------------------
# User Model
# -----------------------------
# class User(models.Model):
#     USER_TYPES = [
#         ('member', 'Member'),
#         ('creator', 'Creator'),
#         ('admin', 'Admin'),
#     ]

#     id_user = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=20, choices=USER_TYPES)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     registration_date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

class User(AbstractUser):
    USER_TYPES = [
        ('member', 'Member'),
        ('creator', 'Creator'),
        ('admin', 'Admin'),
    ]
    username = models.CharField(max_length=150, unique=True, default='user_default')
    id_user = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=USER_TYPES)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="notifications")

    def __str__(self):
        return f"Notification {self.notification_id} to {self.user}"


# -----------------------------
# User_Club (Many-to-Many)
# -----------------------------
class UserClub(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'club')

    def __str__(self):
        return f"{self.user} in {self.club}"
