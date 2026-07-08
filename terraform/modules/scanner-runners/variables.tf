variable "name" {
  description = "Name prefix for scanner runner resources."
  type        = string
}

variable "vpc_id" {
  description = "VPC ID the scanner runner instances are launched into."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for the scanner runner Auto Scaling Group."
  type        = list(string)
}

variable "instance_type" {
  description = "EC2 instance type for scanner runner nodes."
  type        = string
  default     = "t3.large"
}

variable "min_size" {
  description = "Minimum number of scanner runner instances."
  type        = number
  default     = 1
}

variable "max_size" {
  description = "Maximum number of scanner runner instances."
  type        = number
  default     = 5
}

variable "desired_capacity" {
  description = "Desired number of scanner runner instances at steady state."
  type        = number
  default     = 1
}

variable "ami_id" {
  description = "AMI ID for scanner runner instances. Defaults to the latest Amazon Linux 2023 AMI."
  type        = string
  default     = ""
}

variable "tags" {
  description = "Additional resource tags."
  type        = map(string)
  default     = {}
}
