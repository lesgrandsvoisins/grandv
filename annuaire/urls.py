from django.urls import path
from .views import keycloak_login, keycloak_login_view

urlpatterns = [
    path('api/login/', keycloak_login, name='keycloak_login'),
    path('login/', keycloak_login_view, name='keycloak_login'),
]
