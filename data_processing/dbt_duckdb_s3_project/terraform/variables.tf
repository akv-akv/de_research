variable "my_ip" {
  description = "My IP address to allow SSH access"
  type        = string
}

variable "my_public_key" {
  description = "My public key to allow SSH access"
  type        = string
}

variable "aws_profile_name" {
  description = "Name of the AWS profile in ~/.aws/config"
  type        = string
}

variable "aws_vpc_name" {
  description = "Name of the VPC in AWS account"
  type        = string
}

variable "aws_s3_bucket_name" {
  description = "Name of the S3 bucket in AWS"
  type        = string
}

variable "docker_image_name" {
  description = "Name of the Docker image"
  type        = string
  default     = "dbt_duckdb_s3_project"
}