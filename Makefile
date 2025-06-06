# App: AWS Customer CRUD
# Package: project_root
# File: Makefile
# Version: 0.0.8
# Author: Bobwares
# Date: Fri Jun 06 02:53:56 UTC 2025
# Description: Convenience targets for build, test, and deployment.
#

.PHONY: build test plan deploy

build:
	pip install -r requirements.txt

test:
	pytest -q

plan:
	cd iac && terraform init && terraform plan

deploy:
	cd iac && terraform apply -auto-approve
