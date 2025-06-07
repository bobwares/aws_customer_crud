# App: AWS Customer CRUD
# Package: e2e
# File: run_e2e.py
# Version: 0.0.4
# Author: Bobwares
# Date: Sat Jun 07 01:50:52 UTC 2025
# Description: Simple HTTP test for hello world endpoint hitting /customers.
#
import os
import requests

API_BASE = os.getenv('API_BASE', 'https://8z9creg24d.execute-api.us-east-1.amazonaws.com')
API_PATH = os.getenv('API_PATH', '/customers')


def main() -> None:
    url = f"{API_BASE.rstrip('/')}{API_PATH}"
    print('Requesting', url)
    resp = requests.get(url)
    print('Response', resp.status_code, resp.text)
    resp.raise_for_status()


if __name__ == "__main__":
    main()
