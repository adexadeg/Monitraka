from django.urls import path
from .views import LogoutView, ProfileSettingsView, RegisterView, LoginView, UserView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('dashboard', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('profile-settings', ProfileSettingsView.as_view())
]