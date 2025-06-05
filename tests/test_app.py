# App: AWS Customer CRUD
# Package: tests
# File: test_app.py
# Version: 0.0.1
# Author: Bobwares
# Date: Thu Jun 5 14:41:42 UTC 2025
# Description: Unit tests for app module.

import json
from unittest.mock import patch
from src.app import lambda_handler


@patch('src.app.get_dynamodb_client')
@patch('src.app.validate_jwt')
def test_lambda_handler_create_item(mock_validate_jwt, mock_get_dynamodb_client):
    """Test creating an item."""
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
    """Test retrieving a non-existent item."""
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
