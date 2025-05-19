# ldap_service.py

import logging
import ldap
from ldap import modlist as modlist
from django.conf import settings

logger = logging.getLogger(__name__)


class LDAPService:
    def __init__(self):
        self.ldap_url = settings.LDAP_CONFIG["URL"]
        self.base_dn = settings.LDAP_CONFIG["BASE_DN"]
        self.bind_dn = settings.LDAP_CONFIG["BIND_DN"]
        self.bind_password = settings.LDAP_CONFIG["BIND_PASSWORD"]
        self.users_ou = settings.LDAP_CONFIG["USERS_OU"]
        self.groups_ou = settings.LDAP_CONFIG["GROUPS_OU"]

    def _connect(self):
        logger.debug(f"[LDAP] Connecting to {self.ldap_url}")
        conn = ldap.initialize(self.ldap_url)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        return conn

    def authenticate(self, username, password):
        user_dn = "cn=%s,%s" % (username,self.users_ou)
        logger.debug(f"[LDAP] Authentication initiated for for {user_dn}")
        try:
            conn = self._connect()
            conn.simple_bind_s(user_dn, password)
            logger.debug(f"[LDAP] Authentication succeeded for {username}")
            # conn.simple_bind_s(self.bind_dn, self.bind_password)
            # search_filter = f"(uid={username})"
            # result = conn.search_s(self.base_dn, ldap.SCOPE_SUBTREE, search_filter)
            return {"username":username}
        except ldap.INVALID_CREDENTIALS:
            logger.warning(f"[LDAP] Invalid credentials for {username}")
            raise Exception(f"[LDAP] Invalid credentials for {username}")

    def search_user(self, username):
        conn = self._connect()
        conn.simple_bind_s(self.bind_dn, self.bind_password)
        search_filter = f"(uid={username})"
        result = conn.search_s(self.base_dn, ldap.SCOPE_SUBTREE, search_filter)
        logger.debug(f"[LDAP] Search result for {username}: {len(result)} match(es)")
        return result

    def create_user(self, username, password, email, firstname, lastname):
        if self.search_user(username):
            raise Exception(f"User '{username}' already exists.")

        conn = self._connect()
        conn.simple_bind_s(self.bind_dn, self.bind_password)

        dn = "cn=%s,%s" % (username,self.users_ou)
        # f"cn={username},ou={self.users_ou},{self.base_dn}"
        attrs = {
            "objectClass": [b"inetOrgPerson", b"organizationalPerson", b"top"],
            "cn": [username.encode()],
            "givenName": [firstname],
            "sn": [lastname],
            "uid": [email],
            "userPassword": [password.encode()]
        }

        ldif = modlist.addModlist(attrs)
        conn.add_s(dn, ldif)
        logger.debug(f"[LDAP] Created user {username} with DN {dn}")
        return dn
