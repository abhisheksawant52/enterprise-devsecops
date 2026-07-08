aws_region  = "us-east-1"
environment = "prod"

vpc_id             = "vpc-00000000000000001"
private_subnet_ids = ["subnet-00000000000000002", "subnet-00000000000000003", "subnet-00000000000000004"]

scanner_instance_type = "t3.xlarge"
scanner_min_capacity  = 3
scanner_max_capacity  = 10

findings_retention_days = 365

tags = {
  Owner      = "platform-security"
  CostCenter = "eng-platform-prod"
}
