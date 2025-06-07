# App: AWS Customer CRUD
# Package: e2e
# File: run_e2e.py
# Version: 0.0.2
# Author: Bobwares
# Date: Sat Jun 07 01:41:18 UTC 2025
# Description: Simple HTTP test for hello world endpoint.
#
import os
import requests

API_BASE = os.getenv('API_BASE', 'https://8z9creg24d.execute-api.us-east-1.amazonaws.com')


def main() -> None:
    resp = requests.get(f"{API_BASE}/")
    print('GET', resp.status_code, resp.text)
    resp.raise_for_status()


if __name__ == "__main__":
    main()
