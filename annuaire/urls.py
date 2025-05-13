from django.urls import path
from .views import keycloak_login, keycloak_login_view, keycloak_logout_view

urlpatterns = [
    path('api/login/', keycloak_login, name='keycloak_login'),
    path('login/', keycloak_login_view, name='keycloak_login'),
]

urlpatterns += [
    path('logout/', keycloak_logout_view, name='keycloak_logout'),
]