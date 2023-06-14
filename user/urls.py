from django.urls import path
from django.contrib.auth import views as auth_views
from user.views import RegisterView, ProfileView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration-page'),
    path('login/', auth_views.LoginView.as_view(template_name='event/login.html'), name='login-page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout-page'),
    path('profile/', ProfileView.as_view(), name='profile-page')
]