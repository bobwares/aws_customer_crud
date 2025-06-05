# App: AWS Customer CRUD
# Package: tests
# File: test_models.py
# Version: 0.0.1
# Author: Bobwares
# Date: Thu Jun 5 14:41:42 UTC 2025
# Description: Unit tests for models module.

from src.models import Item


def test_item_serialization():
    """Test serialization and deserialization of Item."""
    item = Item(id="1", name="Test Item", description="This is a test.")
    dynamodb_item = item.to_dynamodb()
    new_item = Item.from_dynamodb(dynamodb_item)
    assert new_item == item
