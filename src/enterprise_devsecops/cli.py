"""`edsec` command-line interface.

Provides operator-facing subcommands for running scans, inspecting
policy, and evaluating deployment gate decisions without going through
the HTTP service.
"""

from __future__ import annotations

import json
import logging
import sys

import click

from enterprise_devsecops import __version__
from enterprise_devsecops.config import get_settings
from enterprise_devsecops.gate import DeploymentGate
from enterprise_devsecops.logging_config import configure_logging
from enterprise_devsecops.models import Finding
from enterprise_devsecops.policy import PolicyEngine
from enterprise_devsecops.scanning import SCANNER_REGISTRY

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__, prog_name="edsec")
def main() -> None:
    """enterprise-devsecops command-line interface."""
    settings = get_settings()
    configure_logging(level=settings.log_level, json_output=settings.log_json)


@main.group()
def scan() -> None:
    """Run scanners against a target."""


@scan.command("run")
@click.argument("target")
@click.option(
    "--type",
    "scan_types",
    multiple=True,
    default=("sast", "sca", "container"),
    help="Scanner categories to run. May be repeated.",
)
@click.option("--output", type=click.Choice(["text", "json"]), default="text")
def scan_run(target: str, scan_types: tuple[str, ...], output: str) -> None:
    """Run one or more scanners against TARGET and print findings."""
    settings = get_settings()
    findings: list[Finding] = []
    for scan_type in scan_types:
        scanner_cls = SCANNER_REGISTRY.get(scan_type)
        if scanner_cls is None:
            raise click.ClickException(f"unknown scan type: {scan_type}")
        scanner = scanner_cls(timeout_seconds=settings.scanner_timeout_seconds)
        findings.extend(scanner.scan(target))

    if output == "json":
        click.echo(json.dumps([f.model_dump(mode="json") for f in findings], indent=2))
    else:
        if not findings:
            click.echo(f"No findings for {target}.")
        for finding in findings:
            click.echo(f"[{finding.severity.value}] {finding.scanner}: {finding.title}")


@main.group()
def policy() -> None:
    """Inspect and validate organization security policy."""


@policy.command("show")
@click.option("--path", default=None, help="Path to policy YAML; defaults to configured path.")
def policy_show(path: str | None) -> None:
    """Print the resolved policy document."""
    settings = get_settings()
    engine = PolicyEngine.from_yaml(path or settings.policy_path)
    click.echo(engine.policy.model_dump_json(indent=2))


@policy.command("validate")
@click.option("--path", default=None, help="Path to policy YAML; defaults to configured path.")
def policy_validate(path: str | None) -> None:
    """Validate that the policy document parses correctly."""
    settings = get_settings()
    try:
        PolicyEngine.from_yaml(path or settings.policy_path)
    except Exception as exc:  # noqa: BLE001
        raise click.ClickException(f"invalid policy: {exc}") from exc
    click.echo("Policy is valid.")


@main.group()
def gate() -> None:
    """Evaluate deployment gate decisions."""


@gate.command("evaluate")
@click.argument("target")
@click.option(
    "--type",
    "scan_types",
    multiple=True,
    default=("sast", "sca", "container"),
    help="Scanner categories to run before gating.",
)
@click.option("--policy-path", default=None, help="Path to policy YAML.")
def gate_evaluate(target: str, scan_types: tuple[str, ...], policy_path: str | None) -> None:
    """Scan TARGET and evaluate the deployment gate decision.

    Exits with a non-zero status code when the gate denies the deployment,
    making this suitable for use directly in a CI/CD pipeline step.
    """
    settings = get_settings()
    findings: list[Finding] = []
    for scan_type in scan_types:
        scanner_cls = SCANNER_REGISTRY.get(scan_type)
        if scanner_cls is None:
            raise click.ClickException(f"unknown scan type: {scan_type}")
        scanner = scanner_cls(timeout_seconds=settings.scanner_timeout_seconds)
        findings.extend(scanner.scan(target))

    engine = PolicyEngine.from_yaml(policy_path or settings.policy_path)
    decision = DeploymentGate(engine).decide(findings)

    click.echo(decision.model_dump_json(indent=2))
    if not decision.allowed:
        sys.exit(1)


if __name__ == "__main__":
    main()
