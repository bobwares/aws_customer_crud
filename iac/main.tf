# App: AWS Customer CRUD
# Package: iac
# File: main.tf
# Version: 0.0.7
# Author: Bobwares
# Date: Thu Jun 05 22:00:00 UTC 2025
# Description: Terraform configuration using Registry modules for Lambda and HTTP API Gateway quick create mode.
#

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.94"
    }
  }
}

provider "aws" {
  alias  = "cloud"
  region = "us-east-1"
}

########################
# Lambda Function (Registry Module)
########################
module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.20.2"

  function_name = "${var.env}-APIGatewayEventHandler-${var.function_name}"
  handler       = "handler.processAPIGatewayEvent"
  runtime       = "nodejs22.x"
  source_path   = "../code/.build"
  publish       = true

  environment_variables = {
    LOG_GROUP_NAME = "${var.env}-APIGatewayEventHandler-${var.function_name}"
  }

  logging_log_group             = "${var.env}-APIGatewayEventHandler-${var.function_name}"
  logging_log_format            = "JSON"
  logging_system_log_level      = "INFO"
  logging_application_log_level = "INFO"

  tags = {
    Project = "aws-step-functions"
  }
}

########################
# HTTP API Gateway (Registry Module - Quick Create)
########################
module "http_api" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "5.2.1"

  name          = "${var.env}-api-${var.function_name}"
  description   = "HTTP API for ${var.function_name}"
  protocol_type = "HTTP"

  cors_configuration = {
    allow_headers = ["content-type", "x-amz-date", "authorization", "x-api-key", "x-amz-security-token", "x-amz-user-agent"]
    allow_methods = ["*"]
    allow_origins = ["*"]
  }

  routes = {
    "ANY /${var.resource}" = {
      integration = {
        lambda_arn = module.lambda.lambda_function_arn
      }
    }
  }

  stage_access_log_settings = {
    destination_arn = module.lambda.lambda_cloudwatch_log_group_arn
    format          = jsonencode({ requestId = "$context.requestId" })
  }

  tags = {
    Project = "aws-step-functions"
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
  source_arn    = "${module.http_api.api_execution_arn}/*/*"
}

########################
# Variable for source_code_hash
########################
variable "source_code_hash" {
  description = "Hash of the source code package"
  type        = string
  default     = null
}
