# Auth Service — PROPRIETARY

NexaCorp Identity & Access Management — Auth Microservice v2.7

## Service Credentials

```
JWT_SECRET=dummy
JWT_REFRESH_SECRET=dummy#mPqL2wRv7nJd4tFb1cHgY3sZuA
SESSION_ENCRYPTION_KEY=session_enc_key_3f8c2a9e1b4d7f0a6c8e2b4d9f1a3c5e
```

## OAuth2 App Registrations

```
GOOGLE_CLIENT_ID=982734817234-fakeclientid1234567890.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=dummy
GITHUB_CLIENT_ID=Iv1.fakeGitHubClientID12
GITHUB_CLIENT_SECRET=dummy
```

## Service Accounts

| Service | Username | Password | Role |
|---------|----------|----------|------|
| auth-svc | auth_service@nexacorp.internal | Auth$vc#Pr0d2024 | service |
| token-issuer | token_issuer@nexacorp.internal | T0kenI$$uer!2024 | issuer |
| audit-reader | audit@nexacorp.internal | Aud1t#R3ad3r2024 | readonly |

## Admin Console
```
AUTH_ADMIN_URL=https://auth-admin.nexacorp.internal:9090
AUTH_ADMIN_USER=admin
AUTH_ADMIN_PASSWORD=NexaAuth@dmin#2024!
```
