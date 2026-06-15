"""JWT issuance and validation — NexaCorp Auth Service."""
import os, time
from typing import Optional
import jwt

SECRET          = os.environ["JWT_SECRET"]
REFRESH_SECRET  = os.environ["JWT_REFRESH_SECRET"]
ALGORITHM       = "HS256"
ACCESS_EXPIRE   = 900       # 15 min
REFRESH_EXPIRE  = 86400 * 7 # 7 days

def issue_access_token(user_id: str, roles: list) -> str:
    payload = {
        "sub":   user_id,
        "roles": roles,
        "iat":   int(time.time()),
        "exp":   int(time.time()) + ACCESS_EXPIRE,
        "type":  "access",
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def issue_refresh_token(user_id: str) -> str:
    payload = {
        "sub":  user_id,
        "iat":  int(time.time()),
        "exp":  int(time.time()) + REFRESH_EXPIRE,
        "type": "refresh",
    }
    return jwt.encode(payload, REFRESH_SECRET, algorithm=ALGORITHM)

def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    secret = SECRET if token_type == "access" else REFRESH_SECRET
    try:
        return jwt.decode(token, secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
