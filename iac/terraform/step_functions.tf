# App: AWS Customer CRUD
# Package: iac.terraform
# File: step_functions.tf
# Version: 0.0.4
# Author: Bobwares
# Date: Thu Jun 05 20:20:35 UTC 2025
# Description: Step Functions state machine for orchestrating CRUD operations.

resource "aws_iam_role" "sfn_role" {
  name = "step_functions_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "states.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "sfn_policy" {
  name   = "step_functions_policy"
  role   = aws_iam_role.sfn_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["lambda:InvokeFunction"]
      Resource = aws_lambda_function.crud_function.arn
    }]
  })
}

resource "aws_sfn_state_machine" "crud_state_machine" {
  name     = "crudStateMachine"
  role_arn = aws_iam_role.sfn_role.arn
  definition = jsonencode({
    Comment = "Customer CRUD workflow"
    StartAt = "ValidateInput"
    States = {
      ValidateInput = {
        Type     = "Task"
        Resource = aws_lambda_function.crud_function.arn
        Parameters = {
          action   = "validate"
          "payload.$" = "$"
        }
        Next = "DetermineOperation"
      }
      DetermineOperation = {
        Type = "Choice"
        Choices = [
          {
            Variable     = "$.httpMethod"
            StringEquals = "POST"
            Next         = "Create"
          },
          {
            Variable     = "$.httpMethod"
            StringEquals = "GET"
            Next         = "Read"
          },
          {
            Variable     = "$.httpMethod"
            StringEquals = "PUT"
            Next         = "Update"
          },
          {
            Variable     = "$.httpMethod"
            StringEquals = "DELETE"
            Next         = "Delete"
          }
        ]
        Default = "Unsupported"
      }
      Create = {
        Type     = "Task"
        Resource = aws_lambda_function.crud_function.arn
        Parameters = {
          action   = "create"
          "payload.$" = "$"
        }
        End = true
      }
      Read = {
        Type     = "Task"
        Resource = aws_lambda_function.crud_function.arn
        Parameters = {
          action   = "read"
          "payload.$" = "$"
        }
        End = true
      }
      Update = {
        Type     = "Task"
        Resource = aws_lambda_function.crud_function.arn
        Parameters = {
          action   = "update"
          "payload.$" = "$"
        }
        End = true
      }
      Delete = {
        Type     = "Task"
        Resource = aws_lambda_function.crud_function.arn
        Parameters = {
          action   = "delete"
          "payload.$" = "$"
        }
        End = true
      }
      Unsupported = {
        Type  = "Fail"
        Error = "UnsupportedMethod"
        Cause = "Only CRUD methods are supported."
      }
    }
  })
}
