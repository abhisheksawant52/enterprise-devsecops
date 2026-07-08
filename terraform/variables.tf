variable "aws_region" {
  description = "AWS region the platform infrastructure is deployed into."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment name (dev, staging, prod)."
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Short name used to prefix created resources."
  type        = string
  default     = "enterprise-devsecops"
}

variable "vpc_id" {
  description = "VPC ID the scanner runners and supporting resources are deployed into."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used for scanner runner instances."
  type        = list(string)
}

variable "scanner_instance_type" {
  description = "EC2 instance type used for scanner runner nodes."
  type        = string
  default     = "t3.large"
}

variable "scanner_min_capacity" {
  description = "Minimum number of scanner runner instances."
  type        = number
  default     = 1
}

variable "scanner_max_capacity" {
  description = "Maximum number of scanner runner instances."
  type        = number
  default     = 5
}

variable "findings_retention_days" {
  description = "Number of days scan reports/findings are retained in object storage."
  type        = number
  default     = 90
}

variable "tags" {
  description = "Additional resource tags applied across all modules."
  type        = map(string)
  default     = {}
}
