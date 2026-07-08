"""Container image vulnerability scanner.

Wraps an image-scanning tool (e.g. Trivy, Grype) to find vulnerable OS
packages and misconfigurations in built container images before they are
promoted through the deployment gate.
"""

from __future__ import annotations

import logging

from enterprise_devsecops.models import Finding, Severity
from enterprise_devsecops.scanning.base import Scanner

logger = logging.getLogger(__name__)


class ContainerScanner(Scanner):
    """Scans a container image reference for known vulnerabilities.

    A real implementation shells out to a tool such as Trivy, e.g.::

        subprocess.run(
            ["trivy", "image", "--format", "json", "--quiet", target],
            capture_output=True,
            timeout=self.timeout_seconds,
            check=False,
        )

    and maps each vulnerability entry to a `Finding`.
    """

    name = "container"

    def scan(self, target: str) -> list[Finding]:
        """Scan the container image at `target`.

        Args:
            target: Fully-qualified image reference, e.g.
                `registry.example.com/team/app:1.2.3`.

        Returns:
            A list of findings. This stub returns an empty list; concrete
            deployments replace this with real image-scan output parsing.
        """
        logger.info("Container scan requested for %s (stub: no findings)", target)
        return []

    @staticmethod
    def _to_finding(raw: dict) -> Finding:
        """Translate a single raw vulnerability entry into a `Finding`."""
        return Finding(
            scanner=ContainerScanner.name,
            severity=Severity(raw.get("severity", "MEDIUM").upper()),
            title=raw.get("title", "Vulnerable image layer"),
            description=raw.get("description", ""),
            resource=raw.get("image", "unknown"),
            cve_id=raw.get("cve_id"),
        )
