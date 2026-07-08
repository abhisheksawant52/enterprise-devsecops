"""Static Application Security Testing (SAST) scanner.

Wraps a source-code static analysis tool (e.g. Semgrep) to produce
`Finding` objects for the policy engine and deployment gate.
"""

from __future__ import annotations

import logging

from enterprise_devsecops.models import Finding, Severity
from enterprise_devsecops.scanning.base import Scanner

logger = logging.getLogger(__name__)


class SastScanner(Scanner):
    """Runs static analysis over a repository checkout.

    In a real deployment this shells out to a tool such as Semgrep or
    CodeQL, e.g.::

        subprocess.run(
            ["semgrep", "--config", "auto", "--json", target],
            capture_output=True,
            timeout=self.timeout_seconds,
            check=False,
        )

    and parses the tool's JSON report into `Finding` objects. The
    invocation is left as a documented stub so this package has no hard
    runtime dependency on a specific SAST binary.
    """

    name = "sast"

    def scan(self, target: str) -> list[Finding]:
        """Scan the repository checkout at `target` for code-level issues.

        Args:
            target: Filesystem path to the repository checkout.

        Returns:
            A list of findings. This stub returns an empty list; concrete
            deployments replace this with real tool output parsing.
        """
        logger.info("SAST scan requested for %s (stub: no findings)", target)
        return []

    @staticmethod
    def _to_finding(raw: dict) -> Finding:
        """Translate a single raw tool result into a `Finding`.

        Kept as a separate, testable method so the JSON-to-model mapping
        can be unit tested independently of invoking the real tool.
        """
        return Finding(
            scanner=SastScanner.name,
            severity=Severity(raw.get("severity", "MEDIUM").upper()),
            title=raw.get("title", "Untitled SAST finding"),
            description=raw.get("description", ""),
            resource=raw.get("path", "unknown"),
            rule_id=raw.get("rule_id"),
        )
