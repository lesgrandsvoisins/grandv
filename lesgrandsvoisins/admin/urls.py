from django.urls import path
from .views import keycloak_login, keycloak_login_view, keycloak_logout_view, dashboard_view, index_view, keycloak_register_view, check_username # , ldap_login_view, ldap_login, ldap_logout_view, ldap_register_view

urlpatterns = [
    # path('api/login/', keycloak_login, name='keycloak_login'),
    path('login/', keycloak_login_view, name='keycloak_login'),
    path('dashboard/', dashboard_view, name='lesgrandsvoisins_dashboard'),
    path('', index_view, name="lesgrandsvoisins_admin" )
]

urlpatterns += [
    path('logout/', keycloak_logout_view, name='keycloak_logout'),
]

urlpatterns += [
    path("register/", keycloak_register_view, name="keycloak_register"),
    path("ajax/check-username/", check_username, name="check_username")
]


