"""Employee data model — NexaCorp HR System."""
from dataclasses import dataclass, field
from typing import Optional
import hashlib, os

@dataclass
class Employee:
    employee_id: str
    full_name: str
    email: str
    department: str
    salary: float
    manager_id: Optional[str] = None
    _ssn_hash: str = field(default="", repr=False)

    def set_ssn(self, ssn: str) -> None:
        salt = os.environ.get("SSN_SALT", "nexacorp_salt_v1")
        self._ssn_hash = hashlib.sha256(f"{salt}{ssn}".encode()).hexdigest()

    def verify_ssn(self, ssn: str) -> bool:
        salt = os.environ.get("SSN_SALT", "nexacorp_salt_v1")
        return self._ssn_hash == hashlib.sha256(f"{salt}{ssn}".encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "employee_id": self.employee_id,
            "full_name": self.full_name,
            "email": self.email,
            "department": self.department,
            "salary": self.salary,
        }
