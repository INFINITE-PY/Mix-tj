from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Channel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='channel')
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    duration = models.CharField(max_length=10, default="00:00")  # Формат 01:59:03
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"