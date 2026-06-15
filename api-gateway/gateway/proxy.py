"""Reverse-proxy routing layer — NexaCorp API Gateway."""
import os, time, hashlib, hmac
import httpx

MASTER_KEY = os.environ.get("GATEWAY_MASTER_KEY", "")

ROUTES = {
    "/payments":      os.environ.get("PAYMENTS_UPSTREAM",      "http://payments-svc:8080"),
    "/notifications": os.environ.get("NOTIFICATIONS_UPSTREAM", "http://notif-svc:8081"),
    "/analytics":     os.environ.get("ANALYTICS_UPSTREAM",     "http://analytics-svc:8082"),
    "/search":        os.environ.get("SEARCH_UPSTREAM",        "http://search-svc:8083"),
}

def sign_request(path: str, body: bytes) -> str:
    ts  = str(int(time.time()))
    msg = f"{ts}.{path}.".encode() + body
    sig = hmac.new(MASTER_KEY.encode(), msg, hashlib.sha256).hexdigest()
    return f"t={ts},v1={sig}"

async def proxy(path: str, method: str, headers: dict, body: bytes):
    for prefix, upstream in ROUTES.items():
        if path.startswith(prefix):
            headers["X-Internal-Signature"] = sign_request(path, body)
            async with httpx.AsyncClient() as client:
                resp = await client.request(method, upstream + path,
                                            headers=headers, content=body)
                return resp.status_code, resp.content
    return 404, b"Not Found"
