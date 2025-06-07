# App: AWS Customer CRUD
# Package: tests
# File: test_main_tf.py
# Version: 0.0.2
# Author: Bobwares
# Date: Sat Jun 07 03:08:02 UTC 2025
# Description: Ensure main.tf includes schema directory in Lambda source path.

import os


def test_lambda_source_includes_schema():
    path = os.path.join('iac', 'main.tf')
    with open(path) as f:
        content = f.read()
    assert '../schema' in content


def test_api_gateway_not_module():
    path = os.path.join('iac', 'main.tf')
    with open(path) as f:
        content = f.read()
    assert 'module "http_api"' not in content
    assert 'aws_apigatewayv2_api' in content

