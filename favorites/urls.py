from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('', views.favorites_list, name='list'),
    path('toggle/<int:product_id>/', views.toggle_favorite, name='toggle'),
]
