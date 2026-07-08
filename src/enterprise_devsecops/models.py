"""Core domain models shared across the platform.

These are the data contracts exchanged between scanners, the policy
engine, the deployment gate, and the HTTP/CLI surfaces.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Ordered finding severity."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

    @property
    def rank(self) -> int:
        """Lower rank means more severe; useful for threshold comparisons."""
        order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
            Severity.INFO: 4,
        }
        return order[self]

    def at_least(self, threshold: "Severity") -> bool:
        """Return True if this severity is as severe as, or more than, `threshold`."""
        return self.rank <= threshold.rank


class Finding(BaseModel):
    """A single security finding produced by a scanner."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    scanner: str = Field(description="Name of the scanner that produced this finding.")
    severity: Severity
    title: str
    description: str = ""
    resource: str = Field(description="File path, package, or image reference affected.")
    cve_id: str | None = Field(default=None, description="Associated CVE identifier, if any.")
    rule_id: str | None = Field(default=None, description="Scanner-specific rule identifier.")
    metadata: dict[str, str] = Field(default_factory=dict)
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ScanRequest(BaseModel):
    """A request to scan a repository/artifact for a set of scan types."""

    repository: str = Field(description="Repository identifier, e.g. org/repo.")
    ref: str = Field(default="main", description="Git ref, branch, or tag to scan.")
    scan_types: list[str] = Field(
        default_factory=lambda: ["sast", "sca", "container"],
        description="Which scanner categories to run.",
    )
    requested_by: str = Field(description="User or service account requesting the scan.")


class Policy(BaseModel):
    """Organization security policy evaluated against scan findings."""

    name: str
    version: str = "1.0.0"
    max_severity: Severity = Field(
        default=Severity.HIGH,
        description="The most severe finding allowed without a waiver.",
    )
    fail_on: list[Severity] = Field(
        default_factory=lambda: [Severity.CRITICAL, Severity.HIGH],
        description="Severities that block a deployment gate when unwaived.",
    )
    denied_licenses: list[str] = Field(
        default_factory=list, description="Software licenses that are never permitted."
    )
    waivers: list[str] = Field(
        default_factory=list,
        description="Finding IDs or rule IDs that are explicitly exempted.",
    )


class GateDecision(BaseModel):
    """Outcome of evaluating findings against a policy at a deployment gate."""

    allowed: bool
    reason: str
    policy_name: str
    blocking_findings: list[Finding] = Field(default_factory=list)
    waived_findings: list[Finding] = Field(default_factory=list)
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
