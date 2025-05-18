from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .keycloak_service import KeycloakService

from django.shortcuts import render, redirect
from .forms import KeycloakLoginForm, KeycloakRegistrationForm
from django.contrib import messages

from .models import Application

@csrf_exempt
def keycloak_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        keycloak = KeycloakService()
        try:
            token = keycloak.login(username, password)
            userinfo = keycloak.get_userinfo(token)
            return JsonResponse({
                'token': token,
                'user': userinfo
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)

def keycloak_login_view(request):
    if request.method == 'POST':
        form = KeycloakLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            keycloak = KeycloakService()

            try:
                token = keycloak.login(username, password)
                userinfo = keycloak.get_userinfo(token)
                request.session['access_token'] = token['access_token']
                request.session['refresh_token'] = token['refresh_token']
                request.session['username'] = userinfo.get('preferred_username')
                return redirect('lesgrandsvoisins_dashboard')  # Replace with your destination view
            except Exception as e:
                messages.error(request, f'Login failed: {str(e)}')
    else:
        form = KeycloakLoginForm()
    
    return render(request, 'lesgrandsvoisins/admin/login.html', {'form': form, 'title': 'Login'})

def keycloak_logout_view(request):
    refresh_token = request.session.get('refresh_token')
    if refresh_token:
        try:
            keycloak = KeycloakService()
            keycloak.logout(refresh_token)
        except Exception as e:
            messages.warning(request, f"Keycloak logout error: {e}")
    
    # Clear the session
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('keycloak_login')  # or wherever your login page is

def dashboard_view(request):
    apps = Application.objects.all().order_by("title")
    return render(request, 'lesgrandsvoisins/admin/dashboard.html', {'apps': apps, 'title': 'Tableau de bord'})

def index_view(request):
    if check_logged_in(request):
        return redirect('lesgrandsvoisins_dashboard')
    else:
        return redirect('keycloak_login')

def check_logged_in(request):
    return "username" in request.session

def keycloak_register_view(request):
    if request.method == "POST":
        form = KeycloakRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                keycloak = KeycloakService()
                keycloak.create_user(data["username"], data["password"], data.get("email"), data.get("firstname"), data.get("lastname"))
                messages.success(request, "Registration successful. You may now log in.")
                return redirect("keycloak_login")
            except Exception as e:
                messages.error(request, f"Registration failed: {e}")
    else:
        form = KeycloakRegistrationForm()
    return render(request, "lesgrandsvoisins/admin/register.html", {"form": form, 'title': 'S\'enregistrer'})

def check_username(request):
    username = request.GET.get("username", "").strip()
    keycloak = KeycloakService()
    if username:
        existing_users = keycloak.admin.get_users(query={"username": username})
        return JsonResponse({"available": len(existing_users) == 0})
    return JsonResponse({"available": False})
