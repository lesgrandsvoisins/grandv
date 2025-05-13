from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .keycloak_service import KeycloakService

from django.shortcuts import render, redirect
from .forms import KeycloakLoginForm
from django.contrib import messages


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
                return redirect('dashboard')  # Replace with your destination view
            except Exception as e:
                messages.error(request, f'Login failed: {str(e)}')
    else:
        form = KeycloakLoginForm()
    
    return render(request, 'login.html', {'form': form})
