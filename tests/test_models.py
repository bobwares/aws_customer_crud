# App: AWS Customer CRUD
# Package: tests
# File: test_models.py
# Version: 0.0.2
# Author: Bobwares
# Date: Thu Jun 05 17:10:52 UTC 2025
# Description: Unit tests for models module.

from src.models import Customer, CustomerName


def test_customer_serialization():
    """Test serialization and deserialization of Customer."""
    customer = Customer(
        customerId="1",
        name=CustomerName(first="Test", last="User"),
        primaryEmail="test@example.com",
        createdAt="2025-06-05T00:00:00Z",
        updatedAt="2025-06-05T00:00:00Z",
        status="ACTIVE"
    )
    dynamodb_item = customer.to_dynamodb()
    new_customer = Customer.from_dynamodb(dynamodb_item)
    assert new_customer == customer
