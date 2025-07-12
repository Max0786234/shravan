from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='homepage'),  # guests only
    path('home/', views.home_loggedin, name='home_loggedin'),  # for logged-in users
    path('upload/', views.upload_audio, name='upload_audio'),
    path('audio/<int:pk>/', views.audiobook_detail, name='audiobook_detail'),
    path('favorites/', views.favorites, name='favorites'),
    path('add_favorite/<int:pk>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<int:pk>/', views.remove_favorite, name='remove_favorite'),

    # ✅ Specify where to go after login
    path('login/', auth_views.LoginView.as_view(
        template_name='user/login.html',
        redirect_authenticated_user=True,
        next_page='homepage'  # 👈 This line tells Django to go here after login
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),

    path('register/', views.register, name='register'),
    path('my_uploads/', views.my_uploads, name='my_uploads'),
    path('profile/', views.profile_view, name='profile'),
    path('guest/audio/<int:pk>/', views.audiobook_detail, name='audiobook_detail_guest'),

    
]
