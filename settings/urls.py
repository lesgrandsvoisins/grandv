"""
URL configuration for annuaire project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
# from annuaire import urls as annuaire_urls
from lgvadmin import urls as admin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.admin import urls as wagtailadmin_urls



urlpatterns = [
    path('wagtailadmin/', include(wagtailadmin_urls)),
    path('wagtaildocs/', include(wagtaildocs_urls)),
    path('djangoadmin/', admin.site.urls),
    # path("annuaire/", include(annuaire_urls)),
    path("admin/", include(admin_urls)),
    path("", include(wagtail_urls)),
]
