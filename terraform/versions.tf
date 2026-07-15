terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.54"
    }
  }

  # Remote state backend. Left commented so `terraform init -backend=false`
  # works out of the box for CI validation and local experimentation.
  # Configure per-environment via `-backend-config=environments/<env>/backend.hcl`.
  #
  # backend "s3" {
  #   bucket         = "enterprise-devsecops-tfstate"
  #   key            = "platform/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "enterprise-devsecops-tf-lock"
  #   encrypt        = true
  # }
}
