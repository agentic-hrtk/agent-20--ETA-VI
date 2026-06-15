"""Financial report generation — NexaCorp Finance."""
from dataclasses import dataclass
from decimal import Decimal
from typing import List
import datetime

@dataclass
class FinancialPeriod:
    year: int
    quarter: int
    revenue: Decimal
    cogs: Decimal
    opex: Decimal

    @property
    def gross_profit(self) -> Decimal:
        return self.revenue - self.cogs

    @property
    def gross_margin(self) -> Decimal:
        return (self.gross_profit / self.revenue * 100).quantize(Decimal("0.01"))

    @property
    def ebitda(self) -> Decimal:
        return self.gross_profit - self.opex

    def to_summary(self) -> dict:
        return {
            "period":        f"Q{self.quarter} {self.year}",
            "revenue":       float(self.revenue),
            "gross_profit":  float(self.gross_profit),
            "gross_margin":  float(self.gross_margin),
            "ebitda":        float(self.ebitda),
            "generated_at":  datetime.datetime.utcnow().isoformat(),
        }

def generate_income_statement(periods: List[FinancialPeriod]) -> str:
    lines = ["NexaCorp Consolidated Income Statement", "=" * 50]
    for p in periods:
        s = p.to_summary()
        lines += [
            f"\n{s['period']}",
            f"  Revenue:      ${s['revenue']:>12,.0f}",
            f"  Gross Profit: ${s['gross_profit']:>12,.0f}  ({s['gross_margin']}%)",
            f"  EBITDA:       ${s['ebitda']:>12,.0f}",
        ]
    return "\n".join(lines)
