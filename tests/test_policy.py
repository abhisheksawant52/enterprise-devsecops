"""Tests for the policy engine."""

from enterprise_devsecops.models import Finding, Severity
from enterprise_devsecops.policy import PolicyEngine


def _finding(severity: Severity, rule_id: str | None = None) -> Finding:
    return Finding(
        scanner="sast",
        severity=severity,
        title="Example finding",
        resource="src/app.py",
        rule_id=rule_id,
    )


def test_evaluate_passes_with_no_blocking_findings() -> None:
    engine = PolicyEngine.from_dict(
        {"name": "default", "fail_on": ["CRITICAL", "HIGH"]}
    )
    findings = [_finding(Severity.LOW), _finding(Severity.INFO)]

    assert engine.evaluate(findings) is True


def test_evaluate_fails_on_blocking_severity() -> None:
    engine = PolicyEngine.from_dict(
        {"name": "default", "fail_on": ["CRITICAL", "HIGH"]}
    )
    findings = [_finding(Severity.CRITICAL)]

    assert engine.evaluate(findings) is False


def test_waived_finding_does_not_block() -> None:
    finding = _finding(Severity.CRITICAL, rule_id="rule-123")
    engine = PolicyEngine.from_dict(
        {"name": "default", "fail_on": ["CRITICAL"], "waivers": ["rule-123"]}
    )

    blocking, waived = engine.classify([finding])

    assert blocking == []
    assert waived == [finding]
