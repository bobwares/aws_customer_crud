# AWS Lambda Python DynamoDB CRUD Pattern

### **Table of Contents**

1. [Overview](#overview)
    - [Key Features](#key-features)
    - [Use Cases](#use-cases)
    - [Benefits](#benefits)
2. [Technology Stack](#technology-stack)
3. [Directory Structure](#directory-structure)
4. [Configuration](#configuration)
    - [pyproject.toml](#pyprojecttoml)
    - [config.yaml](#configyaml)
5. [Code](#code)
    - [src/app.py](#srcapppy)
    - [src/models.py](#srcmodelspy)
    - [src/utils.py](#srcutilspy)
6. [Tests](#tests)
    - [tests/test_app.py](#teststest_apppy)
    - [tests/test_models.py](#teststest_modelspy)
7. [CI/CD Pipeline with GitHub Actions](#ci-cd-pipeline-with-github-actions)
8. [Infrastructure as Code (IaC)](#infrastructure-as-code-iac)
    - [Terraform](#terraform)


---

### **Overview**

The **AWS Lambda Python DynamoDB CRUD Pattern** provides a scalable and serverless architecture for building CRUD (Create, Read, Update, Delete) applications using AWS services. This pattern leverages AWS Lambda for executing backend logic, Amazon DynamoDB for data storage, and API Gateway for exposing RESTful APIs. It is designed to facilitate rapid development, deployment, and management of serverless applications with robust security and scalability.

#### **Key Features**

- **Serverless Architecture**: Eliminates the need to manage servers, allowing developers to focus on code.
- **Scalable Data Storage**: Utilizes Amazon DynamoDB for high-performance NoSQL database capabilities.
- **Secure API Endpoints**: Implements JWT authentication for secure access to APIs.
- **Infrastructure as Code**: Uses Terraform and AWS CDK for automated and consistent infrastructure provisioning.

#### **Use Cases**

- **Web Applications**: Backend for single-page applications (SPAs) requiring RESTful APIs.
- **Mobile Applications**: Backend services for mobile apps needing scalable data storage and processing.
- **Microservices**: Building microservices with isolated functions and managed resources.

#### **Benefits**

- **Cost-Efficient**: Pay only for the compute time and resources used, reducing operational costs.
- **Highly Scalable**: Automatically scales with the application's demand without manual intervention.
- **Rapid Deployment**: Enables quick iterations and deployments through CI/CD pipelines.

---

### Technology Stack

- **Programming Languages**:
    - **Python 3.11** for backend logic and AWS Lambda functions.

- **Libraries**:
    - **boto3>=1.26.0**: AWS SDK for Python to interact with AWS services.
    - **pydantic>=1.10.2**: Data validation and settings management using Python type annotations.
    - **aws-lambda-powertools**: Utilities for AWS Lambda functions to enhance observability and development.
    - **python-jose>=3.3.0**: JSON Object Signing and Encryption (JOSE) implementation for JWT token handling.

- **Services/Frameworks**:
    - **AWS Lambda**: Function as a Service (FaaS) for executing backend logic.
    - **Amazon DynamoDB**: NoSQL database for storing application data.
    - **API Gateway**: REST API endpoints for client interactions.
    - **AWS IAM**: Access management and security for AWS resources.
    - **Modern Python Project Structure with pyproject.toml**: Organized project setup for dependency management and configuration.

- **Infrastructure as Code (IaC)**:
    - **Terraform**: Tool for building, changing, and versioning infrastructure safely and efficiently.
    - **AWS CDK**: Infrastructure as Code framework for defining cloud infrastructure using familiar programming languages.

- **Testing**:
    - **Python Unit Testing Tools**: Frameworks like `unittest` or `pytest` for testing code.
    - **.http Files**: HTTP request files for manual or automated API testing.

- **CI/CD**
    - **GitHub Actions**: Automates the software development workflow, including building, testing, and deploying code.

---

### Directory Structure

```
/project-directory
│
├── /src
│   ├── app.py              # Main application entry point
│   ├── models.py           # Data models and schemas
│   ├── utils.py            # Utility functions
│
├── /tests
│   ├── test_app.py         # Tests for app.py
│   ├── test_models.py      # Tests for models.py
│
├── /iac                      # Infrastructure as Code
│   ├── /terraform            # Directory for Terraform configurations
│   ├── main.tf           # Main Terraform configuration
│   ├── variables.tf      # Terraform variables
│   └── outputs.tf        # Terraform outputs
├── pyproject.toml
└── .gitignore
```

---

### Implementation

#### Configuration Files

##### pyproject.toml

```toml
[tool.poetry]
name = "aws-lambda-python-dynamodb-crud"
version = "1.0.0"
description = "A serverless CRUD application using AWS Lambda, DynamoDB, and API Gateway."
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
boto3 = ">=1.26.0"
pydantic = ">=1.10.2"
aws-lambda-powertools = "^1.27.0"
python-jose = ">=3.3.0"

[tool.poetry.dev-dependencies]
pytest = "^7.2.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

##### config.yaml

```yaml
# Configuration for AWS resources and application settings
aws:
  region: "us-east-1"
  lambda:
    timeout: 30
    memory_size: 256
dynamodb:
  table_name: "ExampleTable"
```

---

### Code

#### src/app.py

```python
# src/app.py

import json
from typing import Any, Dict
from models import Item
from utils import get_dynamodb_client, validate_jwt

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for CRUD operations on DynamoDB.
    """
    client = get_dynamodb_client()
    http_method = event['httpMethod']
    path = event['path']
    
    # JWT Authentication
    token = event['headers'].get('Authorization', '').split(' ')[1]
    if not validate_jwt(token):
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Unauthorized'})
        }
    
    if http_method == 'POST' and path == '/items':
        body = json.loads(event['body'])
        item = Item(**body)
        client.put_item(TableName='ExampleTable', Item=item.to_dynamodb())
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Item created'})
        }
    elif http_method == 'GET' and path.startswith('/items/'):
        item_id = path.split('/')[-1]
        response = client.get_item(TableName='ExampleTable', Key={'id': {'S': item_id}})
        item = response.get('Item')
        if item:
            return {
                'statusCode': 200,
                'body': json.dumps(Item.from_dynamodb(item).dict())
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Item not found'})
            }
    elif http_method == 'PUT' and path.startswith('/items/'):
        item_id = path.split('/')[-1]
        body = json.loads(event['body'])
        item = Item(id=item_id, **body)
        client.put_item(TableName='ExampleTable', Item=item.to_dynamodb())
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item updated'})
        }
    elif http_method == 'DELETE' and path.startswith('/items/'):
        item_id = path.split('/')[-1]
        client.delete_item(TableName='ExampleTable', Key={'id': {'S': item_id}})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item deleted'})
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad Request'})
        }
```

#### src/models.py

```python
# src/models.py

from pydantic import BaseModel, Field
from typing import Any, Dict

class Item(BaseModel):
    id: str = Field(..., description="Unique identifier for the item")
    name: str = Field(..., description="Name of the item")
    description: str = Field(..., description="Description of the item")

    def to_dynamodb(self) -> Dict[str, Any]:
        """
        Convert the Item instance to a DynamoDB compatible format.
        """
        return {
            'id': {'S': self.id},
            'name': {'S': self.name},
            'description': {'S': self.description}
        }

    @classmethod
    def from_dynamodb(cls, item: Dict[str, Any]) -> 'Item':
        """
        Create an Item instance from a DynamoDB item.
        """
        return cls(
            id=item['id']['S'],
            name=item['name']['S'],
            description=item['description']['S']
        )
```

#### src/utils.py

```python
# src/utils.py

import boto3
from jose import jwt, JWTError

def get_dynamodb_client():
    """
    Initialize and return a DynamoDB client.
    """
    return boto3.client('dynamodb')

def validate_jwt(token: str) -> bool:
    """
    Validate the JWT token.
    """
    try:
        payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
        return True
    except JWTError:
        return False
```

---

### Tests

#### tests/test_app.py

```python
# tests/test_app.py

import json
from unittest.mock import patch
from src.app import lambda_handler

@patch('src.app.get_dynamodb_client')
@patch('src.app.validate_jwt')
def test_lambda_handler_create_item(mock_validate_jwt, mock_get_dynamodb_client):
    """
    Test creating an item.
    """
    mock_validate_jwt.return_value = True
    mock_client = mock_get_dynamodb_client.return_value
    event = {
        'httpMethod': 'POST',
        'path': '/items',
        'headers': {'Authorization': 'Bearer validtoken'},
        'body': json.dumps({'id': '1', 'name': 'Item1', 'description': 'A test item'})
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 201
    assert json.loads(response['body'])['message'] == 'Item created'
    mock_client.put_item.assert_called_once()

@patch('src.app.get_dynamodb_client')
@patch('src.app.validate_jwt')
def test_lambda_handler_get_item_not_found(mock_validate_jwt, mock_get_dynamodb_client):
    """
    Test retrieving a non-existent item.
    """
    mock_validate_jwt.return_value = True
    mock_client = mock_get_dynamodb_client.return_value
    mock_client.get_item.return_value = {}
    event = {
        'httpMethod': 'GET',
        'path': '/items/999',
        'headers': {'Authorization': 'Bearer validtoken'},
        'body': None
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 404
    assert json.loads(response['body'])['message'] == 'Item not found'
```

#### tests/test_models.py

```python
# tests/test_models.py

from src.models import Item

def test_item_serialization():
    """
    Test serialization and deserialization of Item.
    """
    item = Item(id="1", name="Test Item", description="This is a test.")
    dynamodb_item = item.to_dynamodb()
    new_item = Item.from_dynamodb(dynamodb_item)
    assert new_item == item
```

---

### **CI/CD Pipeline with GitHub Actions**

#### GitHub Actions Workflow

Create the `.github/workflows/ci-cd.yml` file with the following content:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Run tests
        run: poetry run pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy with Terraform
        working-directory: ./iac/terraform
        run: |
          terraform init
          terraform apply -auto-approve

      - name: Deploy with AWS CDK
        working-directory: ./iac/cdk
        run: |
          pip install -r requirements.txt
          cdk deploy --require-approval never
```

---

### Infrastructure as Code (IaC)

This section covers the implementation of IaC using two different approaches: **Terraform** and **AWS CDK**.

#### **Terraform**

The Terraform configuration automates the deployment of AWS resources. Below is an example of provisioning an AWS Lambda function and DynamoDB table.

##### iac/terraform/variables.tf

```hcl
# iac/terraform/variables.tf

# ------------------------------------------------------
# AWS Provider Configuration
# This block configures the AWS provider for Terraform, 
# specifying the region where AWS resources will be provisioned.
# The 'aws_region' variable is defined with a default value.
# ------------------------------------------------------
variable "aws_region" {
  description = "AWS region where the resources will be deployed"
  type        = string
  default     = "us-east-1"
}

# Variable for DynamoDB table name
variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "ExampleTable"
}
```

##### iac/terraform/output.tf

```hcl
# iac/terraform/output.tf

output "api_url" {
  value = aws_api_gateway_rest_api.crud_api.execution_arn
  description = "API Gateway URL for accessing the CRUD operations"
}

output "lambda_function_arn" {
  value = aws_lambda_function.crud_function.arn
  description = "ARN of the Lambda function"
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.example_table.name
  description = "Name of the DynamoDB table"
}
```

##### iac/terraform/main.tf

```hcl
# iac/terraform/main.tf

# -----------------------------------------
# AWS Provider Configuration
# -----------------------------------------
provider "aws" {
  region = var.aws_region
}

# -----------------------------------------
# DynamoDB Table
# -----------------------------------------
resource "aws_dynamodb_table" "example_table" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

# -----------------------------------------
# IAM Role for Lambda Execution
# -----------------------------------------
resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# -----------------------------------------
# IAM Policy Attachment
# -----------------------------------------
resource "aws_iam_policy_attachment" "lambda_policy_attachment" {
  name       = "lambda_policy_attachment"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

# -----------------------------------------
# Lambda Function
# -----------------------------------------
resource "aws_lambda_function" "crud_function" {
  function_name    = "crudFunction"
  runtime          = "python3.11"
  handler          = "app.lambda_handler"
  role             = aws_iam_role.lambda_role.arn
  filename         = "lambda_function_payload.zip"
  source_code_hash = filebase64sha256("lambda_function_payload.zip")
  timeout          = 30
  memory_size      = 256
}

# -----------------------------------------
# API Gateway
# -----------------------------------------
resource "aws_api_gateway_rest_api" "crud_api" {
  name        = "CRUD API"
  description = "API Gateway for CRUD operations"
}

resource "aws_api_gateway_resource" "items_resource" {
  rest_api_id = aws_api_gateway_rest_api.crud_api.id
  parent_id   = aws_api_gateway_rest_api.crud_api.root_resource_id
  path_part   = "items"
}

resource "aws_api_gateway_method" "items_method" {
  rest_api_id   = aws_api_gateway_rest_api.crud_api.id
  resource_id   = aws_api_gateway_resource.items_resource.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.crud_api.id
  resource_id = aws_api_gateway_resource.items_resource.id
  http_method = aws_api_gateway_method.items_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.crud_function.invoke_arn
}

# Allow API Gateway to invoke Lambda
resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.crud_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.crud_api.execution_arn}/*/*"
}
```

##### iac/terraform/lambda_function_payload.zip

*Ensure that the Lambda function code is zipped and placed in the `iac/terraform/` directory as `lambda_function_payload.zip`.*

