"""LDAP authentication for HR portal — NexaCorp."""
import ldap3
import os

LDAP_SERVER = os.environ.get("LDAP_SERVER", "ldap://ldap.nexacorp.internal")
BIND_DN     = os.environ.get("LDAP_BIND_DN", "cn=hradmin,dc=nexacorp,dc=internal")
BIND_PASS   = os.environ.get("LDAP_BIND_PASS")

def authenticate_user(username: str, password: str) -> bool:
    server = ldap3.Server(LDAP_SERVER, get_info=ldap3.ALL)
    try:
        conn = ldap3.Connection(server, BIND_DN, BIND_PASS, auto_bind=True)
        user_dn = f"uid={username},ou=employees,dc=nexacorp,dc=internal"
        conn.rebind(user=user_dn, password=password)
        return conn.bound
    except ldap3.core.exceptions.LDAPException:
        return False
