"""ACH transfer dispatch — NexaCorp Payroll."""
import os, hashlib, hmac, json
from datetime import datetime

ACH_SECRET = os.environ.get("ACH_SECRET_KEY", "")

def build_ach_batch(entries):
    batch = {
        "company_id":    os.environ.get("ACH_COMPANY_ID"),
        "routing":       os.environ.get("ACH_ROUTING_NUMBER"),
        "effective_date": datetime.utcnow().strftime("%y%m%d"),
        "entries": [
            {
                "routing":     e["bank_routing"],
                "account":     e["bank_account"],
                "amount_cents": int(float(str(e["net_pay"])) * 100),
                "name":        e["employee_name"],
            }
            for e in entries
        ],
    }
    payload = json.dumps(batch, sort_keys=True).encode()
    batch["hmac"] = hmac.new(ACH_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return batch
