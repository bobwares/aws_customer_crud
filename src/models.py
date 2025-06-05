# App: AWS Customer CRUD
# Package: src
# File: models.py
# Version: 0.0.1
# Author: Bobwares
# Date: Thu Jun 5 14:41:42 UTC 2025
# Description: Data models for domain entities.

from pydantic import BaseModel, Field
from typing import Any, Dict


class Item(BaseModel):
    """Item model for DynamoDB storage."""

    id: str = Field(..., description="Unique identifier for the item")
    name: str = Field(..., description="Name of the item")
    description: str = Field(..., description="Description of the item")

    def to_dynamodb(self) -> Dict[str, Any]:
        """Convert the Item instance to a DynamoDB compatible format."""
        return {
            "id": {"S": self.id},
            "name": {"S": self.name},
            "description": {"S": self.description}
        }

    @classmethod
    def from_dynamodb(cls, item: Dict[str, Any]) -> "Item":
        """Create an Item instance from a DynamoDB item."""
        return cls(
            id=item["id"]["S"],
            name=item["name"]["S"],
            description=item["description"]["S"]
        )
