# Root module for the enterprise-devsecops platform infrastructure.
#
# Provisions the object storage used to archive scan findings, the ECS
# cluster that runs the orchestration/platform service (deployed via the
# Helm-equivalent task definitions or, for Kubernetes targets, the chart
# under helm/), and delegates scanner compute to the scanner-runners
# module so scan jobs can scale independently of the platform service.

locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

resource "aws_s3_bucket" "findings" {
  bucket = "${local.name_prefix}-findings"
}

resource "aws_s3_bucket_lifecycle_configuration" "findings" {
  bucket = aws_s3_bucket.findings.id

  rule {
    id     = "expire-findings"
    status = "Enabled"

    expiration {
      days = var.findings_retention_days
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "findings" {
  bucket = aws_s3_bucket.findings.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_ecs_cluster" "platform" {
  name = "${local.name_prefix}-platform"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

module "scanner_runners" {
  source = "./modules/scanner-runners"

  name               = "${local.name_prefix}-scanner"
  vpc_id             = var.vpc_id
  private_subnet_ids = var.private_subnet_ids
  instance_type      = var.scanner_instance_type
  min_size           = var.scanner_min_capacity
  max_size           = var.scanner_max_capacity
  tags               = var.tags
}
