# App: AWS Customer CRUD
# Package: project_root
# File: Makefile
# Version: 0.0.12
# Author: Bobwares
# Date: Sat Jun 07 01:10:48 UTC 2025
# Description: Convenience targets for build, test, and deployment.
#

.PHONY: build test e2e plan deploy venv

venv:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install pytest

build: venv

test:
	./venv/bin/pytest -q

e2e: venv
	./venv/bin/python e2e/run_e2e.py

plan:
	cd iac && terraform init -upgrade && terraform plan
	
deploy:
	cd iac  && terraform apply -auto-approve
