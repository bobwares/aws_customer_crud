# App: AWS Customer CRUD
# Package: src
# File: app.py
# Version: 0.0.7
# Author: Bobwares
# Date: Sat Jun 07 01:41:18 UTC 2025
# Description: Simplified AWS Lambda handler returning hello world.
#
import logging
from typing import Any, Dict


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Return hello world for any request."""
    http_method = event.get("httpMethod")
    path = event.get("path")
    logger.info("Received request %s %s", http_method, path)
    return {"statusCode": 200, "body": "hello world"}
