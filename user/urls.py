from django.urls import path
from . import views
from django.conf.urls.static import static  

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  # Activation URL
    path('initial-login/', views.initial_login, name='initial_login'), # Initial login/profile update
]


