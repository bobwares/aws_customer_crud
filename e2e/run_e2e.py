# App: AWS Customer CRUD
# Package: e2e
# File: run_e2e.py
# Version: 0.0.1
# Author: Bobwares
# Date: Sat Jun 07 01:10:31 UTC 2025
# Description: Simple HTTP end-to-end tests using requests.

import os
import json
import requests

API_BASE = os.getenv('API_BASE', 'https://8z9creg24d.execute-api.us-east-1.amazonaws.com')


def main() -> None:
    payload = {
        "customerId": "55555555-5555-5555-5555-555555555555",
        "name": {"first": "Alice", "last": "Smith"},
        "primaryEmail": "alice@example.com",
        "phoneNumbers": [{"label": "mobile", "number": "+14155550005"}],
        "createdAt": "2025-06-05T00:00:00Z",
        "updatedAt": "2025-06-05T00:00:00Z",
        "status": "ACTIVE",
    }

    resp = requests.post(f"{API_BASE}/customers", json=payload)
    print('POST', resp.status_code, resp.text)
    resp.raise_for_status()

    resp = requests.get(f"{API_BASE}/customers/{payload['customerId']}")
    print('GET', resp.status_code, resp.text)
    resp.raise_for_status()


if __name__ == "__main__":
    main()
