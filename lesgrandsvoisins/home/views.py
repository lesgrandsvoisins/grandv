from django.shortcuts import render, redirect
from lesgrandsvoisins.admin.models import Application

def index_view(request):
  context = {'message': 'Bienvenue'}
  context["apps"] = Application.objects.all().order_by("title")
  return render(request, 'lesgrandsvoisins/home/index.html', context)