# App: AWS Customer CRUD
# Package: src
# File: utils.py
# Version: 0.0.2
# Author: Bobwares
# Date: Thu Jun 05 17:10:52 UTC 2025
# Description: Utility functions for AWS interactions.

import boto3
from jose import JWTError, jwt


def get_dynamodb_client():
    """Initialize and return a DynamoDB client."""
    return boto3.client("dynamodb")


def validate_jwt(token: str) -> bool:
    """Validate the JWT token."""
    try:
        jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        return True
    except JWTError:
        return False
