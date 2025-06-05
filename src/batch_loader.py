# App: AWS Customer CRUD
# Package: src
# File: batch_loader.py
# Version: 0.0.2
# Author: Bobwares
# Date: Thu Jun 05 17:10:34 UTC 2025
# Description: Batch load customer data into DynamoDB table.

import json
from pathlib import Path
from typing import Any, Dict, List

import boto3

from .utils import get_dynamodb_client


def load_customers(file_path: str, table_name: str) -> None:
    """Load customers from JSON file into DynamoDB."""
    client = get_dynamodb_client()
    items: List[Dict[str, Any]] = json.loads(Path(file_path).read_text())
    with client.batch_writer(TableName=table_name) as writer:  # type: ignore
        for item in items:
            pk = f"CUSTOMER#{item['customerId']}"
            writer.put_item(Item={
                'pk': {'S': pk},
                'sk': {'S': 'METADATA'},
                'data': {'S': json.dumps(item)}
            })


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Batch load customer data")
    parser.add_argument("file", help="Path to JSON data file")
    parser.add_argument("--table", default="CustomerDomain", help="DynamoDB table name")
    args = parser.parse_args()

    load_customers(args.file, args.table)
