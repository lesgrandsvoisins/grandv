from django.urls import path
from .views import list_accessible_pages

urlpatterns = [
    path('list_pages/', list_accessible_pages, name='list_pages'),
]