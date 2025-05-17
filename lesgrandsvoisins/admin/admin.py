# admin.py
from django.contrib import admin as django_admin
from .models import Application

@django_admin.register(Application)
class ApplicationAdmin(django_admin.ModelAdmin):
    list_display = ("title", "source_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "source_name", "description")

