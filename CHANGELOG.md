# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-08

### Added

- Policy engine, deployment gate, and SAST/SCA/container scanner modules
  under `enterprise_devsecops`.
- `edsec` CLI with `scan`, `policy`, and `gate` subcommands, plus a FastAPI
  orchestration service with `/health`, `/ready`, `/scan`, and `/gate`.
- Terraform root module and `modules/scanner-runners` sub-module for
  platform infrastructure, with `dev` and `prod` environment tfvars.
- Helm chart for deploying the platform service.
- Documentation, CI pipeline, pre-commit hooks, and open-source project files.
