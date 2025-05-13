from settings import settings

if settings.DEBUG and settings.KEYCLOAK_CONFIG.get("USE_DUMMY", True):
    from .dummy_keycloak_service import DummyKeycloakService as KeycloakService
else:
    from keycloak import KeycloakOpenID

    class KeycloakService:
        def __init__(self):
            config = settings.KEYCLOAK_CONFIG
            self.keycloak_openid = KeycloakOpenID(
                server_url=config["SERVER_URL"],
                client_id=config["CLIENT_ID"],
                realm_name=config["REALM"],
                client_secret_key=config.get("CLIENT_SECRET_KEY", None),
                verify=True  # Set False if self-signed
            )

        def login(self, username, password):
            return self.keycloak_openid.token(username, password)

        def get_userinfo(self, token):
            return self.keycloak_openid.userinfo(token['access_token'])

        def logout(self, refresh_token):
            return self.keycloak_openid.logout(refresh_token)

        def introspect_token(self, token):
            return self.keycloak_openid.introspect(token['access_token'])

        def logout(self, refresh_token):
            return self.keycloak_openid.logout(refresh_token)