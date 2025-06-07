# App: AWS Customer CRUD
# Package: iac
# File: variables.tf
# Version: 0.0.10
# Author: Bobwares
# Date: Fri Jun 06 22:00:36 UTC 2025

# Description: Input variables for Lambda and API Gateway configuration.
#

variable "env" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "function_name" {
  description = "Logical name of the Lambda function"
  type        = string
  default     = "EventProcessor"
}

variable "resource" {
  description = "API Gateway resource path"
  type        = string
  default     = "customers"
}

variable "app_name" {
  description = "Application name used for resource naming"
  type        = string
  default     = "customer-domain"
}

