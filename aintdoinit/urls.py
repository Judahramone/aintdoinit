from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('toggle_dark_mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
]