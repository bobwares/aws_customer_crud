# App: AWS Customer CRUD
# Package: iac
# File: main.tf
# Version: 0.0.19
# Author: Bobwares
# Date: Sat Jun 07 03:07:26 UTC 2025
# Description: Lambda + HTTP API without random suffixes or unsupported inputs.
#

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 5.99.1"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
}

########################
# Lambda Function
########################
module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.20.2"

  function_name = "${var.app_name}-${var.env}-lambda-${var.function_name}"
  handler       = "app.lambda_handler"
  runtime       = "python3.11"
  source_path   = ["../src", "../schema"]
  publish       = true

  # Default role created by the module already has AWSLambdaBasicExecutionRole
  create_role = true

  environment_variables = {
    LOG_GROUP_NAME = "${var.app_name}-${var.env}-lambda-${var.function_name}"
  }

  logging_log_group             = "${var.app_name}-${var.env}-lambda-${var.function_name}"
  logging_log_format            = "JSON"
  logging_system_log_level      = "INFO"
  logging_application_log_level = "INFO"

  tags = {
    Project = "aws-step-functions"
  }
}

########################
# HTTP API Gateway without module
########################
resource "aws_apigatewayv2_api" "http_api" {
  name          = "${var.app_name}-${var.env}-api-${var.function_name}"
  description   = "HTTP API for ${var.function_name}"
  protocol_type = "HTTP"

  cors_configuration {
    allow_headers = [
      "content-type",
      "x-amz-date",
      "authorization",
      "x-api-key",
      "x-amz-security-token",
      "x-amz-user-agent"
    ]
    allow_methods = ["*"]
    allow_origins = ["*"]
  }

  tags = {
    Project = "aws-step-functions"
  }
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id                 = aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = module.lambda.lambda_function_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /${var.resource}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "proxy" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /${var.resource}/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = module.lambda.lambda_cloudwatch_log_group_arn
    format          = jsonencode({ requestId = "$context.requestId" })
  }
}

########################
# Lambda Permission for API Gateway
########################
resource "aws_lambda_permission" "allow_apigateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}
