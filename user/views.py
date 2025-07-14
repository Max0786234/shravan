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
        return redirect('home_loggedin')  # redirect to a separate view
    else:
        query = request.GET.get('q')
        if query:
            audiobooks = Audiobook.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(genre__icontains=query)
            ).distinct()
        else:
            audiobooks = Audiobook.objects.all()
    
        return render(request, 'user/guest_home.html', {'audiobooks': audiobooks})

    
@login_required(login_url='login')

def home_loggedin(request):
    audiobooks = Audiobook.objects.all()
    return render(request, 'user/home_loggedin.html', {'audiobooks': audiobooks})


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
    favorite_items = Favorite.objects.filter(user=request.user).select_related('audiobook')
    return render(request, 'user/favorites.html', {'favorites': favorite_items})


@login_required
def my_uploads(request):
    audiobooks = Audiobook.objects.filter(uploaded_by=request.user)
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
