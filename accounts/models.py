from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )
    
    THEME_CHOICES = (
        ('default', 'Default'),
        ('neon', 'Neon'),
        ('soft', 'Soft'),
        ('blue', 'blue'),
        ('navy', 'navy'),
        ('yelgreen', 'yelgreen'),
    )

    
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    hobi = models.CharField(max_length=100, blank=True)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='default')
    dark_mode = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.username

    @property
    def profile_picture(self):
        if self.image:
            return self.image.url
        return "/media/default.jpg"

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} → {self.following}"

class AdminLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_actions")
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target_actions")
    
    action = models.CharField(max_length=50)  # ban, unban, delete, role_change
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin} -> {self.action} -> {self.target_user}"
