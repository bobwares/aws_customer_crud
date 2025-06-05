# App: AWS Customer CRUD
# Package: src
# File: app.py
# Version: 0.0.2
# Author: Bobwares
# Date: Thu Jun 05 17:10:52 UTC 2025
# Description: AWS Lambda handler for CRUD operations on DynamoDB.

import json
from typing import Any, Dict
from .models import Customer
from .utils import get_dynamodb_client, validate_jwt


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda handler for CRUD operations."""
    client = get_dynamodb_client()
    http_method = event["httpMethod"]
    path = event["path"]
    token = event["headers"].get("Authorization", "").split(" ")[1]
    if not validate_jwt(token):
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Unauthorized"})
        }
    table = "CustomerDomain"

    if http_method == "POST" and path == "/customers":
        body = json.loads(event["body"])
        item = Customer(**body)
        client.put_item(TableName=table, Item=item.to_dynamodb())
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Customer created"})
        }
    if http_method == "GET" and path.startswith("/customers/"):
        item_id = path.split("/")[-1]
        pk = f"CUSTOMER#{item_id}"
        response = client.get_item(TableName=table, Key={"pk": {"S": pk}, "sk": {"S": "METADATA"}})
        item = response.get("Item")
        if item:
            return {
                "statusCode": 200,
                "body": json.dumps(Customer.from_dynamodb(item).dict())
            }
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Customer not found"})
        }
    if http_method == "PUT" and path.startswith("/customers/"):
        item_id = path.split("/")[-1]
        body = json.loads(event["body"])
        item = Customer(customerId=item_id, **body)
        client.put_item(TableName=table, Item=item.to_dynamodb())
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Customer updated"})
        }
    if http_method == "DELETE" and path.startswith("/customers/"):
        item_id = path.split("/")[-1]
        pk = f"CUSTOMER#{item_id}"
        client.delete_item(TableName=table, Key={"pk": {"S": pk}, "sk": {"S": "METADATA"}})
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Customer deleted"})
        }
    return {
        "statusCode": 400,
        "body": json.dumps({"message": "Bad Request"})
    }
