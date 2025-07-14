from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Audiobook  # make sure this model exists

GENRE_CHOICES = [
    ("", "Select Genre"),

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

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AudioUploadForm(forms.ModelForm):
    genre = forms.ChoiceField(
        choices=GENRE_CHOICES,
        required=True,
        label="Genre",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
     
    class Meta:
        model = Audiobook
        fields = ['title', 'author', 'description', 'audio_file', 'cover_image', 'genre']

