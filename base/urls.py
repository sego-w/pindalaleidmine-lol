from django.urls import path
from .views import homepage_view, CalculateAreaView, description

urlpatterns = [
    path('', homepage_view, name='home'),
    path('description/', description, name='description'),
    path('calculate_area/', CalculateAreaView.as_view(), name='calculate_area'),
]