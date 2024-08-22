terraform {
  required_version = ">= 1.0"
}

# Get the current AWS account ID
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

# Get private subnet id from VPC module
data "aws_vpc" "selected" {
  filter {
    name   = "tag:Name"
    values = ["akv-vpc"]
  }
}
data "aws_subnet" "selected" {
  filter {
    name   = "tag:Name"
    values = ["akv-vpc-public-${data.aws_region.current.name}a"]
  }
}

# Security Group for SSH access
#trivy:ignore:avd-aws-0104 - Allow outbout traffic to internet
resource "aws_security_group" "ssh_access" {
  name        = "ssh_access"
  description = "Allow SSH inbound traffic"
  vpc_id      = data.aws_vpc.selected.id

  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.my_ip}/32"] # Allows SSH access from anywhere; restrict this to your IP for better security
  }

  # ingress {
  #   from_port   = 443
  #   to_port     = 443
  #   protocol    = "tcp"
  #   cidr_blocks = ["${var.my_ip}/0"] # Allows SSH access from anywhere; restrict this to your IP for better security
  # }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ssh_access"
  }
}

# Create a new key pair
resource "aws_key_pair" "ec2_key" {
  key_name   = "ec2_key"
  public_key = file(var.my_public_key) # Replace with the path to your public key
}

resource "aws_instance" "ec2_with_s3_ecr_access" {
  ami           = "ami-073fe6857949c14bd"
  instance_type = "t2.micro"
  subnet_id     = data.aws_subnet.selected.id

  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.ssh_access.id]
  key_name                    = aws_key_pair.ec2_key.key_name

  # Enforce IMDSv2
  metadata_options {
    http_tokens = "required"
  }

  # Encrypt the root block device
  root_block_device {
    volume_type           = "gp2"
    volume_size           = 8
    delete_on_termination = true
    encrypted             = true
  }

  # User data script to pull the Docker image from ECR and run it
  user_data = <<-EOF
  #!/bin/bash
  yum update -y
  amazon-linux-extras install docker -y
  service docker start

  # Authenticate Docker to the ECR registry
  $(aws ecr get-login-password --region ${data.aws_region.current.name} | docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com)

  # Pull the Docker image from ECR
  docker pull ${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/akv_dbt_project:latest

  # Run the Docker container
  # docker run -d --name my_container ${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/akv_dbt_project:latest
  EOF

  tags = {
    Name = "EC2 with S3 and ECR Access"
  }
}

# IAM Role for EC2 with S3 and ECR Access
resource "aws_iam_role" "ec2_s3_ecr_role" {
  name = "ec2_s3_ecr_access_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# S3 Access Policy
resource "aws_iam_policy" "s3_access_policy" {
  name        = "s3_access_policy"
  description = "Policy to allow EC2 to read from one S3 prefix and write to another"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:ListAllMyBuckets",
          "s3:ListBucket",
          "s3:GetObject"
        ],
        "Resource" : "*"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject"
        ],
        Resource = [
          "arn:aws:s3:::de-research/data/dbt_duckdb/processed/*"
        ]
      },
    ]
  })
}

# Attach S3 Access Policy to IAM Role
resource "aws_iam_role_policy_attachment" "s3_policy_attach" {
  role       = aws_iam_role.ec2_s3_ecr_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

# Attach ECR Access Policy to IAM Role
resource "aws_iam_role_policy_attachment" "ecr_policy_attach" {
  role       = aws_iam_role.ec2_s3_ecr_role.name
  policy_arn = aws_iam_policy.ecr_access_policy.arn
}


# IAM Policy to allow EC2 to pull images from ECR
resource "aws_iam_policy" "ecr_access_policy" {
  name        = "ecr_access_policy"
  description = "Policy to allow EC2 to pull images from ECR"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:GetAuthorizationToken"
        ],
        Resource = ["arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/akv_dbt_project"]
        #Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "ecr:GetAuthorizationToken"
        ],
        Resource = "*"
      },
    ]
  })
}


# IAM Instance Profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.ec2_s3_ecr_role.name
}

# ECR Repository
#trivy:ignore:avd-aws-0033 - Suggestion to use CustomerManagedKey
#trivy:ignore:avd-aws-0031 - For test purposes tags are MUTABLE
resource "aws_ecr_repository" "akv_dbt_project" {
  name = "akv_dbt_project"
  force_delete         = true

  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}
