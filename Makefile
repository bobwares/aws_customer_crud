# App: AWS Customer CRUD
# Package: project_root
# File: Makefile
# Version: 0.0.10
# Author: Bobwares
# Date: Fri Jun 06 23:59:00 UTC 2025
# Description: Convenience targets for build, test, and deployment.
#

.PHONY: build test plan deploy venv

venv:
        python3 -m venv venv
        ./venv/bin/pip install -r requirements.txt

build: venv

test:
	pytest -q

plan:
	cd iac && terraform init -upgrade && terraform plan

deploy:
	cd iac && terraform init -upgrade && terraform apply -auto-approve
