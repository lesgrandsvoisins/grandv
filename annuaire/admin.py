# admin.py
from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("title", "source_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "source_name", "description")

