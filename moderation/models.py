from django.db import models
from django.conf import settings
from blog.models import Post
from forum.models import Thread

User = settings.AUTH_USER_MODEL


class Report(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("resolved", "Resolved"),
    )

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE)

    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reporter}"