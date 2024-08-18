provider "aws" {
  region = "eu-central-1"
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
        Effect = "Allow",
        Action = [
          "s3:GetObject"
        ],
        Resource = [
          "arn:aws:s3:::de_research/read-prefix/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject"
        ],
        Resource = [
          "arn:aws:s3:::de_research/write-prefix/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::de_research"
        ],
        Condition = {
          "StringLike" : {
            "s3:prefix" : [
              "read-prefix/",
              "write-prefix/"
            ]
          }
        }
      }
    ]
  })
}

# Attach S3 Access Policy to IAM Role
resource "aws_iam_role_policy_attachment" "s3_policy_attach" {
  role       = aws_iam_role.ec2_s3_ecr_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

# ECR Access Policy
resource "aws_iam_policy" "ecr_access_policy" {
  name        = "ECRAccessPolicy"
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
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}

# Attach ECR Access Policy to IAM Role
resource "aws_iam_role_policy_attachment" "ecr_policy_attach" {
  role       = aws_iam_role.ec2_s3_ecr_role.name
  policy_arn = aws_iam_policy.ecr_access_policy.arn
}

# IAM Instance Profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.ec2_s3_ecr_role.name
}

# EC2 Instance with S3 and ECR Access
resource "aws_instance" "ec2_with_s3_ecr_access" {
  ami           = "ami-073fe6857949c14bd" # Replace with the latest AMI ID
  instance_type = "t2.micro"

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

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
  $(aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin <your_ecr_registry_url>)

  # Pull the Docker image from ECR
  docker pull <your_ecr_registry_url>/<your_ecr_repository>:<your_image_tag>

  # Run the Docker container
  docker run -d --name my_container <your_ecr_registry_url>/<your_ecr_repository>:<your_image_tag>
  EOF

  tags = {
    Name = "EC2 with S3 and ECR Access"
  }
}

# ECR Repository
#trivy:ignore:avd-aws-0033 - Suggestion to use CustomerManagedKey
resource "aws_ecr_repository" "akv_dbt_project" {
  name = "akv_dbt_project"

  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}
