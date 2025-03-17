from django.urls import path
from . import views
from django.conf.urls.static import static  # Import for serving media files in development
urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]

