"""Software Composition Analysis (SCA) scanner.

Wraps a dependency vulnerability scanner (e.g. pip-audit, OSV-Scanner) to
identify known-vulnerable third-party packages and license violations.
"""

from __future__ import annotations

import logging

from enterprise_devsecops.models import Finding, Severity
from enterprise_devsecops.scanning.base import Scanner

logger = logging.getLogger(__name__)


class ScaScanner(Scanner):
    """Scans a project's declared dependencies for known vulnerabilities.

    A real implementation shells out to a tool such as `pip-audit` or
    `osv-scanner`, e.g.::

        subprocess.run(
            ["osv-scanner", "--format", "json", f"--lockfile={target}"],
            capture_output=True,
            timeout=self.timeout_seconds,
            check=False,
        )

    and maps each reported advisory to a `Finding`, including the CVE
    identifier where available.
    """

    name = "sca"

    def scan(self, target: str) -> list[Finding]:
        """Scan the dependency manifest/lockfile at `target`.

        Args:
            target: Path to a lockfile (e.g. `requirements.txt`,
                `poetry.lock`) or a repository root containing one.

        Returns:
            A list of findings. This stub returns an empty list; concrete
            deployments replace this with real advisory-feed lookups.
        """
        logger.info("SCA scan requested for %s (stub: no findings)", target)
        return []

    @staticmethod
    def _to_finding(raw: dict) -> Finding:
        """Translate a single raw advisory result into a `Finding`."""
        return Finding(
            scanner=ScaScanner.name,
            severity=Severity(raw.get("severity", "MEDIUM").upper()),
            title=raw.get("title", "Vulnerable dependency"),
            description=raw.get("description", ""),
            resource=raw.get("package", "unknown"),
            cve_id=raw.get("cve_id"),
        )
