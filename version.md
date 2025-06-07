# Version History

## 0.0.1 - Thu Jun 5 14:41:42 UTC 2025
- Initial project structure with Lambda CRUD application, tests, Terraform, and configuration files.

## 0.0.2 - Thu Jun 05 17:12:05 UTC 2025
- Added single table DynamoDB design with CustomerDomain table.
- Updated application code and tests for Customer model.
- Added batch loader script and sample dataset.

## 0.0.3 - Thu Jun 05 17:58:25 UTC 2025
- Integrated jsonschema validation for customer payloads.
- Updated test data to conform to customer_domain schema.
- Updated application and configuration versions.

## 0.0.4 - Thu Jun 05 20:20:35 UTC 2025
- Added AWS Step Functions state machine for input validation and CRUD operations.
- Introduced application logging.
- Bumped project version to 0.0.4 and updated tests.

## 0.0.5 - Thu Jun 05 21:17:49 UTC 2025
- Added new Terraform configuration using registry modules for Lambda and HTTP API Gateway.
- Bumped project version to 0.0.5.


## 0.0.6 - Thu Jun 05 21:45:11 UTC 2025
- Fixed Terraform configuration for API Gateway module
- Updated outputs to use module output
- Bumped project version to 0.0.6

## 0.0.7 - Thu Jun 05 22:00:00 UTC 2025
- Fixed http_api execution ARN reference for Lambda permission
- Bumped project version to 0.0.7


## 0.0.8 - Fri Jun 06 02:53:56 UTC 2025
- Updated Terraform lambda runtime and API module defaults
- Added Makefile with build/test/deploy commands
- Documented dependencies in requirements.txt
- Bumped project version to 0.0.8

## 0.0.9 - Fri Jun 06 15:56:35 UTC 2025
- Added app_name variable to Terraform for resource naming

## 0.0.10 - Fri Jun 06 16:06:00 UTC 2025
- Added setup.sh script to install Terraform and dependencies
- Created codex.yaml to run setup script on workspace creation
- Updated README with setup instructions

## 0.0.11 - Fri Jun 06 18:58:51 UTC 2025
- Fixed Terraform provider configuration by removing alias from aws provider
- Bumped module version to 0.0.11

## 0.0.12 - Fri Jun 06 21:00:00 UTC 2025
- Added random suffix to Terraform resource names to avoid name collisions during deployment
- Updated provider configuration to include random provider

## 0.0.13 - Fri Jun 06 21:23:54 UTC 2025
- Fixed HTTP API integration URI configuration
- Added payload format version for Lambda integration

## 0.0.14 - Fri Jun 06 22:01:00 UTC 2025
- Added DynamoDB table resource to Terraform configuration
- Output DynamoDB table name

## 0.0.15 - Fri Jun 06 22:25:53 UTC 2025
- Updated step_functions.tf to use module lambda output
- Bumped module version to 0.0.15

## 0.0.16 - Fri Jun 06 23:55:35 UTC 2025
- Removed JWT token authorization from Lambda handler and tests
