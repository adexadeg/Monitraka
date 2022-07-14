from django.urls import path
from . import views

urlpatterns = [
    path('', views.BudgetListAPIView.as_view(), name='buget'),
    path('<int:id>', views.BudgetListAPIView.as_view(), name='buget')
]