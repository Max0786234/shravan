from django.db import models
from django.contrib.auth.models import User

# Audiobook model
class Audiobook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='audiobooks/')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def like_count(self):
        return self.likes.count()

    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audiobook = models.ForeignKey(Audiobook, on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'audiobook')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audiobook = models.ForeignKey(Audiobook, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# Favorite model
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    audiobook = models.ForeignKey(Audiobook, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'audiobook')  # prevent duplicate favorites

    def __str__(self):
        return f"{self.user.username} ❤️ {self.audiobook.title}"
