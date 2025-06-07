# App: AWS Customer CRUD
# Package: project_root
# File: Makefile
# Version: 0.0.13
# Author: Bobwares
# Date: Sat Jun 07 22:35:00 UTC 2025
# Description: Convenience targets for build, test, and deployment.
#

.PHONY: install run test e2e plan deploy
install:
        pip install -r requirements.txt

run:
        streamlit run src/app.py

test:
        pytest -q

build: install

e2e:
        python e2e/run_e2e.py

plan:
	cd iac && terraform init -upgrade && terraform plan
	
deploy:
	cd iac  && terraform apply -auto-approve
