from django.db import models
from django.contrib.auth.models import User

GENRE_CHOICES = [
    ("", "Select Genre Based on Mood"),

    # 🌟 Feel-Good / Uplifting
    ("Feel-Good Fiction", "Feel-Good Fiction"),
    ("Humor", "Humor"),
    ("Inspiration", "Inspiration"),
    ("Self-Help", "Self-Help"),
    ("Romantic Comedy", "Romantic Comedy"),

    # 🧠 Deep Thinking / Reflective
    ("Philosophy", "Philosophy"),
    ("Psychology", "Psychology"),
    ("Biography", "Biography"),
    ("Spirituality", "Spirituality"),

    # 💔 Emotional / Heartfelt
    ("Drama", "Drama"),
    ("Romance", "Romance"),
    ("Coming-of-Age", "Coming-of-Age"),
    ("Tragedy", "Tragedy"),

    # 🌌 Escapism / Imaginative
    ("Fantasy", "Fantasy"),
    ("Science Fiction", "Science Fiction"),
    ("Adventure", "Adventure"),
    ("Dystopian", "Dystopian"),

    # 🧩 Curious / Engaged
    ("Mystery", "Mystery"),
    ("Thriller", "Thriller"),
    ("Detective", "Detective Fiction"),
    ("True Crime", "True Crime"),

    # 😱 Dark / Spooky
    ("Horror", "Horror"),
    ("Dark Fantasy", "Dark Fantasy"),
    ("Supernatural", "Supernatural"),

    # 📚 Informative / Productive
    ("Non-Fiction", "Non-Fiction"),
    ("History", "History"),
    ("Science & Tech", "Science & Tech"),
    ("Productivity", "Productivity"),
    ("Business", "Business"),

    # 🎨 Light & Casual
    ("Short Stories", "Short Stories"),
    ("Poetry", "Poetry"),
    ("Children", "Children"),
    ("Young Adult", "Young Adult"),

    # 🎧 Other
    ("Unknown", "Unknown"),
]

# Audiobook model
class Audiobook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='Unknown')
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
