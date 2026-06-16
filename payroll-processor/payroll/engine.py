"""Payroll computation engine — NexaCorp v3.1.4."""
from decimal import Decimal
from dataclasses import dataclass
from typing import List
import logging

logger = logging.getLogger("payroll.engine")

FEDERAL_TAX_BRACKETS = [
    (Decimal("10275"),  Decimal("0.10")),
    (Decimal("41775"),  Decimal("0.12")),
    (Decimal("89075"),  Decimal("0.22")),
    (Decimal("170050"), Decimal("0.24")),
    (Decimal("215950"), Decimal("0.32")),
    (Decimal("539900"), Decimal("0.35")),
    (Decimal("inf"),    Decimal("0.37")),
]

@dataclass
class PayrollEntry:
    employee_id: str
    gross_pay: Decimal
    federal_tax: Decimal
    state_tax: Decimal
    fica: Decimal
    net_pay: Decimal

def compute_federal_tax(annual_gross: Decimal) -> Decimal:
    tax = Decimal(0)
    prev = Decimal(0)
    for bracket, rate in FEDERAL_TAX_BRACKETS:
        if annual_gross <= prev:
            break
        taxable = min(annual_gross, bracket) - prev
        tax += taxable * rate
        prev = bracket
    return (tax / 26).quantize(Decimal("0.01"))

def compute_fica(gross: Decimal) -> Decimal:
    ss  = min(gross, Decimal("160200") / 26) * Decimal("0.062")
    med = gross * Decimal("0.0145")
    return (ss + med).quantize(Decimal("0.01"))

def run_payroll(entries: List[dict]) -> List[PayrollEntry]:
    results = []
    for e in entries:
        gross  = Decimal(str(e["gross_biweekly"]))
        fed    = compute_federal_tax(gross * 26)
        state  = (gross * Decimal("0.05")).quantize(Decimal("0.01"))
        fica   = compute_fica(gross)
        net    = gross - fed - state - fica
        results.append(PayrollEntry(e["employee_id"], gross, fed, state, fica, net))
        logger.info("Computed payroll for %s: net=%s", e["employee_id"], net)
    return results
