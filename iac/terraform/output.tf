# App: AWS Customer CRUD
# Package: iac.terraform
# File: output.tf
# Version: 0.0.4
# Author: Bobwares
# Date: Thu Jun 05 20:20:35 UTC 2025
# Description: Terraform outputs for AWS resources.

output "api_url" {
  value       = aws_api_gateway_rest_api.crud_api.execution_arn
  description = "API Gateway URL for accessing the CRUD operations"
}

output "lambda_function_arn" {
  value       = aws_lambda_function.crud_function.arn
  description = "ARN of the Lambda function"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.customer_domain.name
  description = "Name of the DynamoDB table"
}

output "state_machine_arn" {
  value       = aws_sfn_state_machine.crud_state_machine.arn
  description = "ARN of the Step Functions state machine"
}
