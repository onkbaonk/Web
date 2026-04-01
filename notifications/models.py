from django.db import models
from django.conf import settings
from django.urls import reverse


class Notification(models.Model):

    NOTIF_TYPES = (
        ('comment', 'Comment'),
        ('reply', 'Reply'),
        ('like', 'Like'),
        ('follow', 'Follow'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )  # penerima

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )

    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES)

    post_slug = models.SlugField(null=True, blank=True)
    thread_id = models.IntegerField(null=True, blank=True)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_url(self):
        if self.post_slug:
            return reverse('post_detail', kwargs={'slug': self.post_slug})
        
        if self.thread_id:
            return reverse('thread_detail', kwargs={'pk': self.thread_id})
        
        return "#"

    @property
    def message(self):
      if self.notif_type == "comment":
          return f"{self.sender.username} mengomentari post kamu"
      if self.notif_type == "reply":
          return f"{self.sender.username} membalas komentar kamu"
      if self.notif_type == "like":
          return f"{self.sender.username} menyukai post kamu"
      if self.notif_type == "follow":
          return f"{self.sender.username} mulai mengikuti kamu"
      
      return "Notifikasi baru"
      
    def __str__(self):
        return f"{self.sender} → {self.user} ({self.notif_type})"