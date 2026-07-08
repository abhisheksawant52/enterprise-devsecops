"""Scanner base class.

Every scanning module (SAST, SCA, container, IaC, secrets, ...) implements
this interface so the orchestration layer (`service.py`, `cli.py`) can run
them polymorphically and collect a uniform list of `Finding` objects.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from enterprise_devsecops.models import Finding

logger = logging.getLogger(__name__)


class Scanner(ABC):
    """Abstract base class for all security scanners."""

    #: Short, stable identifier used in `Finding.scanner` and CLI flags.
    name: str = "base"

    def __init__(self, timeout_seconds: int = 900) -> None:
        self.timeout_seconds = timeout_seconds

    @abstractmethod
    def scan(self, target: str) -> list[Finding]:
        """Run the scan against `target` and return a list of findings.

        Args:
            target: The scan target. Interpretation is scanner-specific:
                a filesystem path for SAST/SCA, an image reference for the
                container scanner, etc.
        """
        raise NotImplementedError

    def _run(self, args: list[str]) -> str:
        """Run an external scanner binary and return its stdout.

        This is a structured stub: concrete scanners document the real
        command they would invoke via `subprocess.run`. Wiring this up to
        an actual tool binary is intentionally left to deployment-specific
        configuration.
        """
        logger.debug("Would execute: %s (timeout=%ss)", " ".join(args), self.timeout_seconds)
        raise NotImplementedError(
            f"{self.__class__.__name__} is a structured stub; wire up a real "
            "subprocess invocation for your CI environment."
        )
