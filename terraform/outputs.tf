output "findings_bucket_name" {
  description = "Name of the S3 bucket storing scan reports and findings."
  value       = aws_s3_bucket.findings.bucket
}

output "findings_bucket_arn" {
  description = "ARN of the S3 bucket storing scan reports and findings."
  value       = aws_s3_bucket.findings.arn
}

output "platform_cluster_name" {
  description = "Name of the ECS cluster hosting the platform orchestration service."
  value       = aws_ecs_cluster.platform.name
}

output "scanner_runner_asg_name" {
  description = "Name of the scanner runner Auto Scaling Group."
  value       = module.scanner_runners.autoscaling_group_name
}

output "scanner_runner_security_group_id" {
  description = "Security group ID attached to scanner runner instances."
  value       = module.scanner_runners.security_group_id
}
