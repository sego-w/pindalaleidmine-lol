from django.urls import path
from .views import ShapeDrawerView

urlpatterns = [
    path('', ShapeDrawerView.as_view(), name='shape_drawer'),
    path('', ShapeDrawerView.as_view(), name='calculate_area'),
]
