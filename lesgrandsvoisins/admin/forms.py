from django import forms
from django.core.exceptions import ValidationError
from .keycloak_service import KeycloakService

class KeycloakLoginForm(forms.Form):
    username = forms.CharField(label="Identifiant d'utilisateur", max_length=150)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

# forms.py
class KeycloakRegistrationForm(forms.Form):
    email = forms.EmailField()
    firstname = forms.CharField(label="Prénom", max_length=150)
    lastname = forms.CharField(label="Nom de famille",max_length=150)
    username = forms.CharField(label="Identifiant d'utilisateur",max_length=150)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Mot de passe (confirmation)", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        firstname = cleaned_data.get("firstname")
        lastname = cleaned_data.get("lastname")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if email and not username:
            username = email.split("@")[0]
            cleaned_data["username"] = username

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")

        # # Check Keycloak for existing username
        # if username:
        #     keycloak = KeycloakService()
        #     existing_users = keycloak.admin.get_users(query={"username": username})
        #     if existing_users:
        #         raise ValidationError(f"Username '{username}' is already taken.")

        return cleaned_data
