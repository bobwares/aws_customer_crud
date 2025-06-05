# App: AWS Customer CRUD
# Package: iac
# File: variables.tf
# Version: 0.0.5
# Author: Bobwares
# Date: Thu Jun 05 21:17:09 UTC 2025
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
  description = "API Gateway resource path (e.g., process)"
  type        = string
  default     = "process"
}
