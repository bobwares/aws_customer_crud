# App: AWS Customer CRUD
# Package: src
# File: utils.py
# Version: 0.0.4
# Author: Bobwares
# Date: Thu Jun 05 20:20:35 UTC 2025
# Description: Utility functions for AWS interactions.

import json
from pathlib import Path
from typing import Any, Dict

import boto3
from jose import JWTError, jwt
from jsonschema import Draft202012Validator


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema/customer_domain.json"
CUSTOMER_SCHEMA = json.loads(SCHEMA_PATH.read_text())
CUSTOMER_VALIDATOR = Draft202012Validator(CUSTOMER_SCHEMA)


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


def validate_customer_schema(data: Dict[str, Any]) -> None:
    """Validate customer payload against JSON schema."""
    CUSTOMER_VALIDATOR.validate(data)
