output "autoscaling_group_name" {
  description = "Name of the scanner runner Auto Scaling Group."
  value       = aws_autoscaling_group.scanner_runners.name
}

output "autoscaling_group_arn" {
  description = "ARN of the scanner runner Auto Scaling Group."
  value       = aws_autoscaling_group.scanner_runners.arn
}

output "security_group_id" {
  description = "Security group ID attached to scanner runner instances."
  value       = aws_security_group.scanner_runners.id
}

output "launch_template_id" {
  description = "ID of the scanner runner launch template."
  value       = aws_launch_template.scanner_runners.id
}
