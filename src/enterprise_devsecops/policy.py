"""Policy engine.

Evaluates findings produced by scanners against an organization security
policy and produces allow / deny / waiver decisions. The engine itself is
gate-agnostic; `gate.py` builds a `GateDecision` on top of it for the
deployment-gate use case.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from enterprise_devsecops.models import Finding, Policy, Severity

logger = logging.getLogger(__name__)


class PolicyEngine:
    """Loads a `Policy` and evaluates findings against it."""

    def __init__(self, policy: Policy) -> None:
        self.policy = policy

    @classmethod
    def from_yaml(cls, path: str | Path) -> "PolicyEngine":
        """Load a policy definition from a YAML file on disk."""
        raw = _load_yaml(path)
        return cls(Policy.model_validate(raw))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PolicyEngine":
        """Load a policy definition from an in-memory mapping."""
        return cls(Policy.model_validate(data))

    def is_waived(self, finding: Finding) -> bool:
        """Return True if a finding is explicitly waived by the policy."""
        return finding.id in self.policy.waivers or (
            finding.rule_id is not None and finding.rule_id in self.policy.waivers
        )

    def classify(self, findings: list[Finding]) -> tuple[list[Finding], list[Finding]]:
        """Split findings into (blocking, waived) according to the policy.

        A finding blocks the policy when its severity is in `fail_on` and
        it has not been explicitly waived.
        """
        blocking: list[Finding] = []
        waived: list[Finding] = []

        for finding in findings:
            if self.is_waived(finding):
                waived.append(finding)
                continue
            if finding.severity in self.policy.fail_on:
                blocking.append(finding)

        return blocking, waived

    def evaluate(self, findings: list[Finding]) -> bool:
        """Return True when `findings` comply with the policy (no blockers)."""
        blocking, _ = self.classify(findings)
        return not blocking

    def worst_severity(self, findings: list[Finding]) -> Severity | None:
        """Return the most severe finding's severity, or None if empty."""
        if not findings:
            return None
        return min(findings, key=lambda f: f.severity.rank).severity


def _load_yaml(path: str | Path) -> dict[str, Any]:
    resolved = Path(path)
    if not resolved.exists():
        logger.warning("Policy file %s not found; using an empty policy document.", resolved)
        return {"name": "default", "version": "1.0.0"}
    with resolved.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}
