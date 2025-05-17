# dummy_keycloak_service.py

class DummyKeycloakService:
    _users = [{"username":"test","password":"test"}]

    def login(self, username, password):
        user = next((u for u in self._users if u["username"] == username), None)
        if user and user["password"] == password:
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
        return {"message": "logged out"}

    def create_user(self, username, password, email=None):
        if any(u["username"] == username for u in self._users):
            raise Exception("Username already exists")
        self._users.append({
            "username": username,
            "password": password,
            "email": email,
        })
        return "dummy-user-id"

    def get_users(self, query):
        username = query.get("username")
        if username:
            return [u for u in self._users if u["username"] == username]
        return self._users

    class admin:
        def get_users(query):
            username = query.get("username")
            if username:
                if username == "test":
                    return [{"username":"test"}]
            return []