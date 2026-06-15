"""OAuth2 provider integrations — NexaCorp Auth."""
import os
import httpx

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

async def exchange_google_code(code: str, redirect_uri: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(GOOGLE_TOKEN_URL, data={
            "code":          code,
            "client_id":     os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "redirect_uri":  redirect_uri,
            "grant_type":    "authorization_code",
        })
        resp.raise_for_status()
        return resp.json()

async def exchange_github_code(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "code":          code,
                "client_id":     os.environ["GITHUB_CLIENT_ID"],
                "client_secret": os.environ["GITHUB_CLIENT_SECRET"],
            },
        )
        resp.raise_for_status()
        return resp.json()
