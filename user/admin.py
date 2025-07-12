from django.contrib import admin
from .models import Audiobook, Favorite  # Import your models

admin.site.register(Audiobook)
admin.site.register(Favorite)
