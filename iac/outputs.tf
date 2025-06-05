# App: AWS Customer CRUD
# Package: iac
# File: outputs.tf
# Version: 0.0.5
# Author: Bobwares
# Date: Thu Jun 05 21:17:09 UTC 2025
# Description: Outputs for Lambda and HTTP API resources.
#

output "lambda_function_name" {
  value       = module.lambda.lambda_function_name
  description = "Deployed Lambda function name"
}

output "api_endpoint" {
  value       = aws_apigatewayv2_api.http_api.api_endpoint
  description = "API Gateway endpoint URL"
}
