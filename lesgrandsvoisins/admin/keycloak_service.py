from settings import settings
import logging

logger = logging.getLogger(__name__)


if settings.DEBUG and settings.KEYCLOAK_CONFIG.get("USE_DUMMY", True):
    from .dummy_keycloak_service import DummyKeycloakService as KeycloakService
else:
    from keycloak import KeycloakOpenID

    class KeycloakService:
        def __init__(self):
            config = settings.KEYCLOAK_CONFIG
            logger.debug(f"[Keycloak] Connecting to realm: {self.realm}")
            self.keycloak_openid = KeycloakOpenID(
                server_url=config["SERVER_URL"],
                client_id=config["CLIENT_ID"],
                realm_name=config["REALM"],
                client_secret_key=config["CLIENT_SECRET_KEY"],
                verify=True  # Set False if self-signed
            )

        def login(self, username, password):
            logger.debug(f"[Keycloak] Attempting login for user: {username}")
            token = self.keycloak_openid.token(username, password)
            logger.debug(f"[Keycloak] Login success, token received")
            return token

        def get_userinfo(self, token):
            return self.keycloak_openid.userinfo(token['access_token'])

        def logout(self, refresh_token):
            return self.keycloak_openid.logout(refresh_token)

        def introspect_token(self, token):
            return self.keycloak_openid.introspect(token['access_token'])

        def logout(self, refresh_token):
            return self.keycloak_openid.logout(refresh_token)

        def create_user(self, username, password, email=None):
            payload = {
                "username": username,
                "enabled": True,
                "credentials": [{
                    "type": "password",
                    "value": password,
                    "temporary": False
                }]
            }
            if email:
                payload["email"] = email

            try:
                user_id = self.admin.create_user(payload)
                logger.debug(f"[Keycloak] User created with ID: {user_id}")
                return user_id
            except Exception as e:
                logger.error(f"[Keycloak] Failed to create user: {e}")
                raise Exception(f"Keycloak registration failed: {e}")
