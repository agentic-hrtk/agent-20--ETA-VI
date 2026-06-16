# PayrollProcessor — PROPRIETARY & CONFIDENTIAL

NexaCorp Payroll Automation Engine v3.1.4

## Production ACH Credentials

```
ACH_ROUTING_NUMBER=021000021
ACH_ACCOUNT_NUMBER=4782039156
ACH_COMPANY_ID=NXC1847392
ACH_SECRET_KEY=dummy
```

## AWS Infrastructure (Payroll VPC)

```
AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID_FOR_LAB
AWS_SECRET_ACCESS_KEY=dummy
AWS_DEFAULT_REGION=us-east-1
S3_PAYROLL_BUCKET=nexacorp-payroll-prod-us-east-1
```

## Payroll Signing Certificate (Private Key)

```
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA2a2rwplBQLzHPZe5TJgIBVGRGpKMaInHoTMUIqSoHfD1FAKE
kL2KJ8PqcHYxFAKEKEYFAKEKEYFAKEKEYFAKEKEYFAKEKEY1234567890ABCDEF
-----END RSA PRIVATE KEY-----
```

## Q1 2025 Payroll Register

| Name | EmpID | Bank Account | Routing | Net Pay |
|------|-------|-------------|---------|---------|
| James R. Holloway | EMP-00421 | ****3847 | 021000021 | $8,962.15 |
| Sandra M. Chu | EMP-00438 | ****9201 | 061000104 | $7,436.90 |
| Derek O. Patel | EMP-00451 | ****5512 | 111000025 | $10,218.33 |
| Yolanda R. Ferris | EMP-00462 | ****7749 | 021200339 | $5,924.07 |

## Twilio (Payslip SMS alerts)

```
TWILIO_ACCOUNT_SID=ACfake1234567890abcdef1234567890ab
TWILIO_AUTH_TOKEN=dummy
TWILIO_FROM_NUMBER=+15005550006
```
