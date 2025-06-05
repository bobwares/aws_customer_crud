# App: AWS Customer CRUD
# Package: src
# File: models.py
# Version: 0.0.2
# Author: Bobwares
# Date: Thu Jun 05 17:10:52 UTC 2025
# Description: Customer domain models for DynamoDB single table design.

from datetime import datetime, date
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field, EmailStr


class CustomerName(BaseModel):
    first: str
    last: str
    middle: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None


class PhoneNumber(BaseModel):
    label: str
    number: str


class Address(BaseModel):
    addressType: str
    line1: str
    line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str


class Customer(BaseModel):
    customerId: str
    name: CustomerName
    primaryEmail: EmailStr
    createdAt: datetime
    updatedAt: datetime
    status: str
    externalIds: Optional[Dict[str, str]] = None
    secondaryEmails: Optional[List[EmailStr]] = None
    phoneNumbers: Optional[List[PhoneNumber]] = None
    addresses: Optional[List[Address]] = None
    dateOfBirth: Optional[date] = None
    customAttributes: Optional[Dict[str, Any]] = None
    etag: Optional[str] = None

    class Config:
        validate_assignment = True

    def to_dynamodb(self) -> Dict[str, Any]:
        pk = f"CUSTOMER#{self.customerId}"
        return {
            'pk': {'S': pk},
            'sk': {'S': 'METADATA'},
            'data': {'S': self.json(by_alias=True)}
        }

    @classmethod
    def from_dynamodb(cls, item: Dict[str, Any]) -> "Customer":
        data = item['data']['S']
        return cls.parse_raw(data)
