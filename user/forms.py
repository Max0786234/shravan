from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Audiobook  # make sure this model exists

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = Audiobook
        fields = ['title', 'author', 'description', 'audio_file', 'cover_image']

