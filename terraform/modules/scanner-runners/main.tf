# Scanner runner fleet.
#
# Provisions an Auto Scaling Group of EC2 instances that pull and execute
# scan jobs (SAST/SCA/container) dispatched by the platform orchestration
# service. Scaling independently of the platform service lets scan
# throughput grow with the number of onboarded repositories/teams.

data "aws_ami" "amazon_linux" {
  count       = var.ami_id == "" ? 1 : 0
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

locals {
  ami_id = var.ami_id != "" ? var.ami_id : data.aws_ami.amazon_linux[0].id
}

resource "aws_security_group" "scanner_runners" {
  name        = "${var.name}-sg"
  description = "Security group for enterprise-devsecops scanner runner instances"
  vpc_id      = var.vpc_id

  egress {
    description = "Allow all outbound (scanners fetch dependencies/advisory feeds)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${var.name}-sg" })
}

resource "aws_launch_template" "scanner_runners" {
  name_prefix   = "${var.name}-lt-"
  image_id      = local.ami_id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.scanner_runners.id]

  metadata_options {
    http_tokens   = "required"
    http_endpoint = "enabled"
  }

  tag_specifications {
    resource_type = "instance"
    tags          = merge(var.tags, { Name = "${var.name}-node" })
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "scanner_runners" {
  name                = "${var.name}-asg"
  vpc_zone_identifier = var.private_subnet_ids
  min_size            = var.min_size
  max_size            = var.max_size
  desired_capacity    = var.desired_capacity

  launch_template {
    id      = aws_launch_template.scanner_runners.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.name}-node"
    propagate_at_launch = true
  }

  dynamic "tag" {
    for_each = var.tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}
