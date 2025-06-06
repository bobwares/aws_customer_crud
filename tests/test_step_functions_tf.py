# App: AWS Customer CRUD
# Package: tests
# File: test_step_functions_tf.py
# Version: 0.0.15
# Author: Bobwares
# Date: Fri Jun 06 22:25:53 UTC 2025
# Description: Ensure step_functions.tf references lambda module outputs.

import os


def test_step_functions_uses_module_lambda():
    path = os.path.join('iac', 'step_functions.tf')
    with open(path) as f:
        content = f.read()
    assert 'module.lambda.lambda_function_arn' in content
