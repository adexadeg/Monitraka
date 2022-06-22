from django.urls import path
from .views import LogoutView, RegisterView, LoginView, UserView
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('dashboard', UserView.as_view()),
    path('logout', LogoutView.as_view())
]