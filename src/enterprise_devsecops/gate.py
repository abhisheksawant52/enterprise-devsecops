"""Deployment gate.

Combines scan findings with the `PolicyEngine` to produce a single
pass/fail `GateDecision` that CI/CD pipelines and deployment tooling can
key off of.
"""

from __future__ import annotations

import logging

from enterprise_devsecops.models import Finding, GateDecision
from enterprise_devsecops.policy import PolicyEngine

logger = logging.getLogger(__name__)


class DeploymentGate:
    """Evaluates whether a deployment may proceed given a set of findings."""

    def __init__(self, engine: PolicyEngine) -> None:
        self.engine = engine

    def decide(self, findings: list[Finding]) -> GateDecision:
        """Evaluate `findings` and return a `GateDecision`.

        The gate denies the deployment when one or more findings are
        classified as blocking (i.e. their severity is in the policy's
        `fail_on` list and they are not covered by a waiver).
        """
        blocking, waived = self.engine.classify(findings)
        allowed = not blocking

        if allowed:
            reason = (
                f"No blocking findings against policy '{self.engine.policy.name}' "
                f"({len(waived)} waived)."
            )
        else:
            reason = (
                f"{len(blocking)} blocking finding(s) violate policy "
                f"'{self.engine.policy.name}'."
            )

        decision = GateDecision(
            allowed=allowed,
            reason=reason,
            policy_name=self.engine.policy.name,
            blocking_findings=blocking,
            waived_findings=waived,
        )
        logger.info(
            "Gate decision: allowed=%s policy=%s blocking=%d waived=%d",
            decision.allowed,
            decision.policy_name,
            len(blocking),
            len(waived),
        )
        return decision
