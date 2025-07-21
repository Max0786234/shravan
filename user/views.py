from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, AudioUploadForm
from .models import Audiobook, Favorite
from django.contrib.auth.models import User
from .models import Like
from django.db.models import Q



# Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home_loggedin')  # ✅ Always go to homepage
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user/login.html')
def logout_view(request):
    logout(request)
    return redirect('homepage')  # redirect to guest homepage after logout


from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('home_loggedin')  # Redirect if user is logged in

    query = request.GET.get('q')
    genres = Audiobook._meta.get_field('genre').choices
    grouped_books = {}

    if query:
        audiobooks = Audiobook.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        ).distinct()
        return render(request, 'user/guest_home.html', {
            'search_active': True,
            'audiobooks': audiobooks,
            'query': query
        })
    else:
        for genre_key, genre_label in genres:
            if genre_key:
                books = Audiobook.objects.filter(genre=genre_key)
                if books.exists():
                    grouped_books[genre_label] = books

        return render(request, 'user/guest_home.html', {
            'search_active': False,
            'grouped_books': grouped_books
        })

    

from django.db.models import Q
from .models import Audiobook


@login_required(login_url='login')
def home_loggedin(request):
    query = request.GET.get('q')
    genres = Audiobook._meta.get_field('genre').choices
    grouped_books = {}

    if query:
        audiobooks = Audiobook.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        ).distinct()
        return render(request, 'user/home_loggedin.html', {
            'search_active': True,
            'audiobooks': audiobooks,
            'query': query,
            'user': request.user
        })

    else:
        # Only use genres that have books
        for genre_key, genre_label in genres:
            if genre_key:  # Skip blank genre
                books_in_genre = Audiobook.objects.filter(genre=genre_key)
                if books_in_genre.exists():
                    grouped_books[genre_key] = books_in_genre  # Use genre_key or genre_label

        return render(request, 'user/home_loggedin.html', {
            'search_active': False,
            'grouped_books': grouped_books,
            'user': request.user
        })


# Upload Audiobook
@login_required(login_url='login')
def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio = form.save(commit=False)
            audio.uploaded_by = request.user  # Automatically assign current user
            audio.save()
            return redirect('home_loggedin')
    else:
        form = AudioUploadForm()
    return render(request, 'user/upload.html', {'form': form})


# Add to Favorites
@login_required(login_url='login')
def add_favorite(request, pk):
    audiobook = get_object_or_404(Audiobook, pk=pk)
    Favorite.objects.get_or_create(user=request.user, audiobook=audiobook)
    return redirect('audiobook_detail', pk=pk)

# Remove from Favorites
@login_required(login_url='login')
def remove_favorite(request, pk):
    audiobook = get_object_or_404(Audiobook, pk=pk)
    Favorite.objects.filter(user=request.user, audiobook=audiobook).delete()
    return redirect('audiobook_detail', pk=pk)

# Show all favorites
@login_required(login_url='login')
def favorites(request):
    query = request.GET.get('q')

    # Get all favorite audiobooks for the current user
    favorite_items = Favorite.objects.filter(user=request.user).select_related('audiobook')

    # If there's a search query, filter the audiobooks inside favorites
    if query:
        favorite_items = favorite_items.filter(
            Q(audiobook__title__icontains=query) |
            Q(audiobook__author__icontains=query) |
            Q(audiobook__genre__icontains=query)
        )

    return render(request, 'user/favorites.html', {'favorites': favorite_items})

@login_required
def my_uploads(request):
    query = request.GET.get('q')
    if query:
        audiobooks = Audiobook.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        ).distinct()
    else:
        audiobooks = Audiobook.objects.all()
    
    return render(request, 'user/my_uploads.html', {'audiobooks': audiobooks})


@login_required
def profile_view(request):
    upload_count = Audiobook.objects.filter(uploaded_by=request.user).count()
    return render(request, 'user/profile.html', {
        'user': request.user,
        'upload_count': upload_count,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Audiobook, Favorite, Like, Comment

def audiobook_detail(request, pk):
    audiobook = get_object_or_404(Audiobook, pk=pk)

    # 🚫 If user is not logged in, show guest version
    if not request.user.is_authenticated:
        return render(request, 'user/audiobook_detail_guest.html', {
            'audiobook': audiobook
        })

    is_favorite = Favorite.objects.filter(user=request.user, audiobook=audiobook).exists()
    is_liked = Like.objects.filter(user=request.user, audiobook=audiobook).exists()

    if request.method == 'POST':
        if 'like' in request.POST:
            Like.objects.get_or_create(user=request.user, audiobook=audiobook)
        elif 'comment' in request.POST:
            text = request.POST.get('comment_text')
            if text:
                Comment.objects.create(user=request.user, audiobook=audiobook, text=text)
        return redirect('audiobook_detail', pk=pk)

    comments = audiobook.comments.select_related('user').order_by('-created_at')

    return render(request, 'user/audiobook_detail.html', {
        'audiobook': audiobook,
        'is_favorite': is_favorite,
        'is_liked': is_liked,
        'comments': comments
    })
