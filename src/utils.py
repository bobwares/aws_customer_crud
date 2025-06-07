# App: AWS Customer CRUD
# Package: src
# File: utils.py
# Version: 0.0.5
# Author: Bobwares
# Date: Fri Jun 06 23:55:35 UTC 2025
# Description: Utility functions for AWS interactions.

import json
from pathlib import Path
from typing import Any, Dict

import boto3
from jsonschema import Draft202012Validator


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema/customer_domain.json"
CUSTOMER_SCHEMA = json.loads(SCHEMA_PATH.read_text())
CUSTOMER_VALIDATOR = Draft202012Validator(CUSTOMER_SCHEMA)


def get_dynamodb_client():
    """Initialize and return a DynamoDB client."""
    return boto3.client("dynamodb")

def validate_customer_schema(data: Dict[str, Any]) -> None:
    """Validate customer payload against JSON schema."""
    CUSTOMER_VALIDATOR.validate(data)
