from django.urls import path, include
from . import views
from django.conf import settings
from django.urls import include


urlpatterns = [
    path('', views.home, name = 'home'),
    path('canvas/', views.canvas_view, name='canvas'),
    path('description', views.description, name = 'mushamusha'),
]