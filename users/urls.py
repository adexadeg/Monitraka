from django.urls import path, include
from .views import LogoutView, RegisterView, LoginView, UserView, PasswordSettingsView, ForgotPasswordView, CreateNewPasswordAPIView, PasswordTokenCheckAPI
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('profile-settings', views.ProfileSettingsViewSet)
#router.register('password', views.PasswordSettingsView)
urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('User', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    #path('profile-settings/<int:pk>/', ProfileSettingsView.as_view()),
    path('change-password/<int:pk>/', PasswordSettingsView.as_view()),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', CreateNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path(r'', include(router.urls))
]