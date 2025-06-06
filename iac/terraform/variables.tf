# App: AWS Customer CRUD
# Package: iac.terraform
# File: variables.tf
# Version: 0.0.2
# Author: Bobwares
# Date: Thu Jun 05 17:10:52 UTC 2025
# Description: Terraform variables for AWS resources.

variable "region" {
  description = "AWS Region"
  type = string
  default = "us-east"
}

variable "app_name" {
  description = "Application Name"
  type = string
  default = "customer-domain"
}

variable "aws_region" {
  description = "AWS region where the resources will be deployed"
  type        = string
  default     = "us-east-1"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "CustomerDomain"
}
