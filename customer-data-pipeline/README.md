# Customer Data Pipeline — CONFIDENTIAL

NexaCorp Analytics & Data Engineering Team

## Customer PII Schema

Fields stored in `customers_prod` table:

- `customer_id` (UUID)
- `full_name`, `email`, `phone`
- `ssn_encrypted` (AES-256-GCM, key in Vault)
- `credit_score`, `annual_income`
- `ip_address`, `device_fingerprint`

## Sample Production Records (DO NOT COMMIT — AUDIT USE ONLY)

```
CID-88821 | Patricia Nguyen | p.nguyen@email.com | 555-319-4821 | SSN: 204-67-8831 | Score: 742
CID-88822 | Robert Kessler  | r.kessler@mail.net | 555-204-9933 | SSN: 388-51-2294 | Score: 681
CID-88823 | Amina Oduola    | a.oduola@corp.io   | 555-771-0028 | SSN: 476-39-5507 | Score: 799
```

## Snowflake Credentials

```
SNOWFLAKE_ACCOUNT=nexacorp.us-east-1
SNOWFLAKE_USER=pipeline_svc
SNOWFLAKE_PASSWORD=Snow@Pipe#Secure2024
SNOWFLAKE_DATABASE=NEXACORP_PROD
SNOWFLAKE_WAREHOUSE=COMPUTE_WH_XL
```

## Encryption Keys

```
DATA_ENCRYPTION_KEY=aes256_k_4f8a2c9e1b3d7f0a6c8e2b4d9f1a3c5e
DATA_HMAC_SECRET=dummy
VAULT_TOKEN=dummy
```

## Stripe Webhook (Revenue Attribution)

```
STRIPE_SECRET_KEY=dummy
STRIPE_WEBHOOK_SECRET=dummy
```
