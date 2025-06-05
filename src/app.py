# App: AWS Customer CRUD
# Package: src
# File: app.py
# Version: 0.0.1
# Author: Bobwares
# Date: Thu Jun 5 14:41:42 UTC 2025
# Description: AWS Lambda handler for CRUD operations on DynamoDB.

import json
from typing import Any, Dict
from .models import Item
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
    if http_method == "POST" and path == "/items":
        body = json.loads(event["body"])
        item = Item(**body)
        client.put_item(TableName="ExampleTable", Item=item.to_dynamodb())
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Item created"})
        }
    if http_method == "GET" and path.startswith("/items/"):
        item_id = path.split("/")[-1]
        response = client.get_item(TableName="ExampleTable", Key={"id": {"S": item_id}})
        item = response.get("Item")
        if item:
            return {
                "statusCode": 200,
                "body": json.dumps(Item.from_dynamodb(item).dict())
            }
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Item not found"})
        }
    if http_method == "PUT" and path.startswith("/items/"):
        item_id = path.split("/")[-1]
        body = json.loads(event["body"])
        item = Item(id=item_id, **body)
        client.put_item(TableName="ExampleTable", Item=item.to_dynamodb())
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item updated"})
        }
    if http_method == "DELETE" and path.startswith("/items/"):
        item_id = path.split("/")[-1]
        client.delete_item(TableName="ExampleTable", Key={"id": {"S": item_id}})
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item deleted"})
        }
    return {
        "statusCode": 400,
        "body": json.dumps({"message": "Bad Request"})
    }
