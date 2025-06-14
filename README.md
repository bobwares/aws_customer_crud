# aws_customer_crud

This project demonstrates the **AWS Lambda Python DynamoDB CRUD Pattern** with
an AWS Step Functions workflow. The state machine validates input, determines
the requested operation, and invokes the Lambda function to perform the CRUD
action. Logging is enabled throughout the application for operational
visibility.

## Development
Run `setup.sh` to install Terraform and Python dependencies. The Codex project automatically executes this script when the workspace is created.

The `Makefile` provides a few convenience targets that run outside a virtual environment:

- `make install` – install Python dependencies
- `make run` – start the Streamlit application
- `make test` – run unit tests
- `make e2e` – run end-to-end HTTP tests
- `make plan` – execute `terraform plan` from the `iac` directory
- `make deploy` – deploy infrastructure with Terraform
