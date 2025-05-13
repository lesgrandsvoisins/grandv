from django.test import TestCase, override_settings

# Create your tests here.

from .keycloak_service import KeycloakService

@override_settings(KEYCLOAK_CONFIG={"USE_DUMMY": True}, DEBUG=True)
class KeycloakServiceTests(TestCase):

    def setUp(self):
        self.service = KeycloakService()

    def test_successful_login(self):
        token = self.service.login("test", "test")
        self.assertIn("access_token", token)
        self.assertEqual(token["access_token"], "dummy-access-token")

    def test_failed_login(self):
        with self.assertRaises(Exception) as context:
            self.service.login("wrong", "credentials")
        self.assertIn("Invalid credentials", str(context.exception))

    def test_get_userinfo_valid_token(self):
        token = {"access_token": "dummy-access-token"}
        userinfo = self.service.get_userinfo(token)
        self.assertEqual(userinfo["preferred_username"], "test")
        self.assertEqual(userinfo["email"], "test@example.com")

    def test_get_userinfo_invalid_token(self):
        with self.assertRaises(Exception):
            self.service.get_userinfo({"access_token": "invalid"})

    def test_logout(self):
        response = self.service.logout("dummy-refresh-token")
        self.assertEqual(response["message"], "logged out")
