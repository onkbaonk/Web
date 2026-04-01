from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Thread(models.Model):
    STATUS = (
        ("open", "Open"),
        ("closed", "Closed"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    content = models.TextField()

    views = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS, default="open")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('thread_detail', kwargs={'pk': self.pk}) # Sesuaikan nama parameter

    def __str__(self):
        return self.title


class Reply(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    # reply ke reply
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author}"