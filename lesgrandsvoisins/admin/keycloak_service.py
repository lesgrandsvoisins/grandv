from django.conf import settings
import logging


logger = logging.getLogger(__name__)


if settings.DEBUG and settings.KEYCLOAK_CONFIG["USE_DUMMY"]:
    from .dummy_keycloak_service import DummyKeycloakService as KeycloakService
else:
    from keycloak import KeycloakOpenID, KeycloakAdmin

    class KeycloakService:
        def __init__(self):
            config = settings.KEYCLOAK_CONFIG
            self.realm = config["REALM"]
            logger.debug(f"[Keycloak] Connecting to realm: {self.realm}")

            self.admin = KeycloakAdmin(
                server_url=config["SERVER_URL"],
                username=config["ADMIN_USERNAME"],
                password=config["ADMIN_PASSWORD"],
                realm_name=self.realm,
                client_id=config.get("ADMIN_CLIENT_ID", "admin-cli"),
                verify=True
            )

            self.keycloak_openid = KeycloakOpenID(
                server_url=config["SERVER_URL"],
                client_id=config["CLIENT_ID"],
                realm_name=self.realm,
                client_secret_key=config.get("CLIENT_SECRET_KEY", None),
                verify=True
            )

        def login(self, username, password):
            logger.debug(f"[Keycloak] Attempting login for user: {username}")
            token = self.keycloak_openid.token(username, password)
            logger.debug(f"[Keycloak] Login success, token received")
            return token

        def get_userinfo(self, token):
            logger.debug("[Keycloak] Getting user info")
            userinfo = self.keycloak_openid.userinfo(token["access_token"])
            logger.debug(f"[Keycloak] User info: {userinfo}")
            return userinfo

        def logout(self, refresh_token):
            logger.debug("[Keycloak] Logging out")
            return self.keycloak_openid.logout(refresh_token)

        def introspect_token(self, token):
            return self.keycloak_openid.introspect(token['access_token'])

        def logout(self, refresh_token):
            return self.keycloak_openid.logout(refresh_token)

        def create_user(self, username, password, email, firstname, lastname):
            logger.debug(f"[Keycloak] Creating user: {username}")
            payload = {
                "username": username,
                "email": email,
                "firstName": firstname,
                "lastName": lastname,
                "enabled": True,
                # "credentials": [{
                #     "type": "password",
                #     "value": password,
                #     "temporary": False
                # }]
            }

            try:
                user_id = self.admin.create_user(payload)
                logger.debug(f"[Keycloak] User created with ID: {user_id}")
                return user_id
            except Exception as e:
                logger.error(f"[Keycloak] Failed to create user: {e}")
                raise

        def get_users(self, query):
            logger.debug(f"[Keycloak] Searching for users with query: {query}")
            users = self.admin.get_users(query=query)
            logger.debug(f"[Keycloak] Found {len(users)} user(s)")
            return users