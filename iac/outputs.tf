# App: AWS Customer CRUD
# Package: iac
# File: outputs.tf
# Version: 0.0.8
# Author: Bobwares
# Date: Fri Jun 06 22:00:53 UTC 2025
# Description: Outputs for Lambda and HTTP API resources.
#

output "lambda_function_name" {
  value       = module.lambda.lambda_function_name
  description = "Deployed Lambda function name"
}

output "api_endpoint" {
  value       = module.http_api.api_endpoint
  description = "API Gateway endpoint URL"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.customer_domain.name
  description = "Name of the DynamoDB table"
}
