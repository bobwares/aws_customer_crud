# App: AWS Customer CRUD
# Package: tests
# File: test_app.py
# Version: 0.0.7
# Author: Bobwares
# Date: Sat Jun 07 01:41:18 UTC 2025
# Description: Unit tests for hello world Lambda handler.
#
from unittest.mock import patch

from src.app import lambda_handler


@patch('src.app.logger')
def test_lambda_handler_returns_hello_world(mock_logger):
    """Verify lambda_handler returns hello world."""
    event = {'httpMethod': 'GET', 'path': '/'}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert response['body'] == 'hello world'
    mock_logger.info.assert_called_with('Received request %s %s', 'GET', '/')
