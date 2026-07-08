aws_region  = "us-east-1"
environment = "dev"

vpc_id             = "vpc-00000000000000000"
private_subnet_ids = ["subnet-00000000000000000", "subnet-11111111111111111"]

scanner_instance_type = "t3.medium"
scanner_min_capacity  = 1
scanner_max_capacity  = 2

findings_retention_days = 30

tags = {
  Owner      = "platform-security"
  CostCenter = "eng-platform-dev"
}
