"""HTTP orchestration service.

A thin FastAPI application exposing the platform's scanning orchestration
and deployment-gate decisions to other services and CI/CD pipelines.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from enterprise_devsecops import __version__
from enterprise_devsecops.config import get_settings
from enterprise_devsecops.gate import DeploymentGate
from enterprise_devsecops.logging_config import configure_logging
from enterprise_devsecops.models import Finding, GateDecision, ScanRequest
from enterprise_devsecops.policy import PolicyEngine
from enterprise_devsecops.scanning import SCANNER_REGISTRY

logger = logging.getLogger(__name__)

settings = get_settings()
configure_logging(level=settings.log_level, json_output=settings.log_json)

app = FastAPI(
    title="enterprise-devsecops",
    description="Centralized security policy, scanning orchestration, and deployment gating.",
    version=__version__,
)


class HealthResponse(BaseModel):
    status: str
    version: str


class ScanResponse(BaseModel):
    repository: str
    ref: str
    findings: list[Finding]


class GateRequest(BaseModel):
    findings: list[Finding]


@app.get("/health", response_model=HealthResponse, tags=["operations"])
def health() -> HealthResponse:
    """Liveness probe: process is up and able to serve requests."""
    return HealthResponse(status="ok", version=__version__)


@app.get("/ready", response_model=HealthResponse, tags=["operations"])
def ready() -> HealthResponse:
    """Readiness probe: dependencies (policy file, config) are loadable."""
    try:
        PolicyEngine.from_yaml(settings.policy_path)
    except Exception as exc:  # noqa: BLE001 - surfaced as a 503 for the probe
        raise HTTPException(status_code=503, detail=f"not ready: {exc}") from exc
    return HealthResponse(status="ready", version=__version__)


@app.post("/scan", response_model=ScanResponse, tags=["scanning"])
def run_scan(request: ScanRequest) -> ScanResponse:
    """Orchestrate the requested scanner categories against a repository."""
    findings: list[Finding] = []
    for scan_type in request.scan_types:
        scanner_cls = SCANNER_REGISTRY.get(scan_type)
        if scanner_cls is None:
            raise HTTPException(status_code=400, detail=f"unknown scan type: {scan_type}")
        scanner = scanner_cls(timeout_seconds=settings.scanner_timeout_seconds)
        findings.extend(scanner.scan(request.repository))

    logger.info(
        "Scan orchestrated for %s@%s: %d finding(s) across %s",
        request.repository,
        request.ref,
        len(findings),
        request.scan_types,
    )
    return ScanResponse(repository=request.repository, ref=request.ref, findings=findings)


@app.post("/gate", response_model=GateDecision, tags=["gating"])
def evaluate_gate(request: GateRequest) -> GateDecision:
    """Evaluate a set of findings against the org policy and return a decision."""
    engine = PolicyEngine.from_yaml(settings.policy_path)
    gate = DeploymentGate(engine)
    return gate.decide(request.findings)
