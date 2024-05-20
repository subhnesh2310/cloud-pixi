"""user_auth_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_auth_system.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView

urlpatterns = [
    path('api/user/admin/', admin.site.urls),
    path('api/user/register/', UserRegistrationView.as_view(), name='register'),
    path('api/user/login/', UserLoginView.as_view(), name='login'),
    path('api/user/profile/', UserProfileView.as_view(), name='profile'),
    path('api/user/changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('api/user/send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('api/user/reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    
]
