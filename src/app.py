# App: AWS Customer CRUD
# Package: src
# File: app.py
# Version: 0.0.6
# Author: Bobwares
# Date: Sat Jun 07 01:26:19 UTC 2025
# Description: AWS Lambda handler for CRUD operations on DynamoDB.

import json
import logging
from typing import Any, Dict
from .models import Customer
from .utils import get_dynamodb_client, validate_customer_schema


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda handler for CRUD operations."""
    client = get_dynamodb_client()
    http_method = event["httpMethod"]
    path = event["path"]
    logger.info("Received request %s %s", http_method, path)
    table = "CustomerDomain"

    if http_method == "POST" and path == "/customers":
        body = json.loads(event["body"])
        validate_customer_schema(body)
        item = Customer(**body)
        logger.info("Creating customer %s", item.customerId)
        client.put_item(TableName=table, Item=item.to_dynamodb())
        logger.info("Customer created %s", item.customerId)
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Customer created"})
        }
    if http_method == "GET" and path == "/customers":
        logger.info("Returning hello world for get customers")
        return {
            "statusCode": 200,
            "body": "hello world"
        }
    if http_method == "GET" and path.startswith("/customers/"):
        item_id = path.split("/")[-1]
        pk = f"CUSTOMER#{item_id}"
        logger.info("Fetching customer %s", item_id)
        response = client.get_item(TableName=table, Key={"pk": {"S": pk}, "sk": {"S": "METADATA"}})
        item = response.get("Item")
        if item:
            logger.info("Customer found %s", item_id)
            return {
                "statusCode": 200,
                "body": json.dumps(Customer.from_dynamodb(item).dict())
            }
        logger.info("Customer not found %s", item_id)
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Customer not found"})
        }
    if http_method == "PUT" and path.startswith("/customers/"):
        item_id = path.split("/")[-1]
        body = json.loads(event["body"])
        validate_customer_schema(body | {"customerId": item_id})
        item = Customer(customerId=item_id, **body)
        logger.info("Updating customer %s", item_id)
        client.put_item(TableName=table, Item=item.to_dynamodb())
        logger.info("Customer updated %s", item_id)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Customer updated"})
        }
    if http_method == "DELETE" and path.startswith("/customers/"):
        item_id = path.split("/")[-1]
        pk = f"CUSTOMER#{item_id}"
        logger.info("Deleting customer %s", item_id)
        client.delete_item(TableName=table, Key={"pk": {"S": pk}, "sk": {"S": "METADATA"}})
        logger.info("Customer deleted %s", item_id)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Customer deleted"})
        }
    logger.info("Unsupported operation: %s %s", http_method, path)
    return {
        "statusCode": 400,
        "body": json.dumps({"message": "Bad Request"})
    }
