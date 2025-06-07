# App: AWS Customer CRUD
# Package: tests
# File: test_app.py
# Version: 0.0.6
# Author: Bobwares
# Date: Sat Jun 07 01:26:19 UTC 2025
# Description: Unit tests for app module.

import json
from unittest.mock import patch
from src.app import lambda_handler


@patch('src.app.logger')
@patch('src.app.get_dynamodb_client')
def test_lambda_handler_create_customer(mock_get_dynamodb_client, mock_logger):
    """Test creating a customer."""
    mock_client = mock_get_dynamodb_client.return_value
    event = {
        'httpMethod': 'POST',
        'path': '/customers',
        'headers': {},
        'body': json.dumps({
            'customerId': '33333333-3333-3333-3333-333333333333',
            'name': {'first': 'Item1', 'last': 'Test'},
            'primaryEmail': 't@example.com',
            'phoneNumbers': [{'label': 'mobile', 'number': '+14155550003'}],
            'status': 'ACTIVE',
            'createdAt': '2025-06-05T00:00:00Z',
            'updatedAt': '2025-06-05T00:00:00Z'
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 201
    assert json.loads(response['body'])['message'] == 'Customer created'
    mock_client.put_item.assert_called_once()
    mock_logger.info.assert_any_call('Creating customer %s', '33333333-3333-3333-3333-333333333333')


@patch('src.app.get_dynamodb_client')
def test_lambda_handler_get_customers(mock_get_dynamodb_client):
    """Test retrieving all customers returns hello world."""
    event = {
        'httpMethod': 'GET',
        'path': '/customers',
        'headers': {},
        'body': None
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert response['body'] == 'hello world'


@patch('src.app.get_dynamodb_client')
def test_lambda_handler_get_customer_not_found(mock_get_dynamodb_client):
    """Test retrieving a non-existent customer."""
    mock_client = mock_get_dynamodb_client.return_value
    mock_client.get_item.return_value = {}
    event = {
        'httpMethod': 'GET',
        'path': '/customers/999',
        'headers': {},
        'body': None
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 404
    assert json.loads(response['body'])['message'] == 'Customer not found'
