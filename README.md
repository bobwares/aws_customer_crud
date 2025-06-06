# aws_customer_crud

This project demonstrates the **AWS Lambda Python DynamoDB CRUD Pattern** with
an AWS Step Functions workflow. The state machine validates input, determines
the requested operation, and invokes the Lambda function to perform the CRUD
action. Logging is enabled throughout the application for operational
visibility.

## Development

The `Makefile` provides a few convenience targets:

- `make build` – install Python dependencies
- `make test` – run unit tests
- `make plan` – execute `terraform plan` from the `iac` directory
- `make deploy` – deploy infrastructure with Terraform
