"""Tests for the deployment gate."""

from enterprise_devsecops.gate import DeploymentGate
from enterprise_devsecops.models import Finding, Severity
from enterprise_devsecops.policy import PolicyEngine


def test_gate_allows_clean_scan() -> None:
    engine = PolicyEngine.from_dict({"name": "org-policy", "fail_on": ["CRITICAL", "HIGH"]})
    gate = DeploymentGate(engine)

    decision = gate.decide([])

    assert decision.allowed is True
    assert decision.policy_name == "org-policy"


def test_gate_denies_on_critical_finding() -> None:
    engine = PolicyEngine.from_dict({"name": "org-policy", "fail_on": ["CRITICAL", "HIGH"]})
    gate = DeploymentGate(engine)
    finding = Finding(
        scanner="container",
        severity=Severity.CRITICAL,
        title="Known-vulnerable base image",
        resource="registry.example.com/app:1.0.0",
    )

    decision = gate.decide([finding])

    assert decision.allowed is False
    assert finding in decision.blocking_findings
