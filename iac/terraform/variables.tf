# App: AWS Customer CRUD
# Package: iac.terraform
# File: variables.tf
# Version: 0.0.1
# Author: Bobwares
# Date: Thu Jun 5 14:41:42 UTC 2025
# Description: Terraform variables for AWS resources.

variable "aws_region" {
  description = "AWS region where the resources will be deployed"
  type        = string
  default     = "us-east-1"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "ExampleTable"
}
