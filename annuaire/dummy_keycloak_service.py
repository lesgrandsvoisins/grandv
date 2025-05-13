# dummy_keycloak_service.py
class DummyKeycloakService:
    def login(self, username, password):
        if username == "test" and password == "test":
            return {
                "access_token": "dummy-access-token",
                "refresh_token": "dummy-refresh-token"
            }
        raise Exception("Invalid credentials")

    def get_userinfo(self, token):
        if token.get("access_token") == "dummy-access-token":
            return {
                "preferred_username": "test",
                "email": "test@example.com",
                "name": "Test User",
                "sub": "dummy-id"
            }
        raise Exception("Invalid token")

    def logout(self, refresh_token):
        # No real action needed for dummy
        return {"message": "logged out"}
