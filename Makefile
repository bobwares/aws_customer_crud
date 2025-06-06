# App: AWS Customer CRUD
# Package: project_root
# File: Makefile
# Version: 0.0.9
# Author: Bobwares
# Date: Fri Jun 06 21:00:00 UTC 2025
# Description: Convenience targets for build, test, and deployment.
#

.PHONY: build test plan deploy

build:
	pip install -r requirements.txt

test:
	pytest -q

plan:
	cd iac && terraform init -upgrade && terraform plan

deploy:
	cd iac && terraform init -upgrade && terraform apply -auto-approve
