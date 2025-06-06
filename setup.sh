# App: AWS Customer CRUD
# Package: project_root
# File: setup.sh
# Version: 0.0.10
# Author: Bobwares
# Date: Fri Jun 06 16:06:00 UTC 2025
# Description: Setup script to install Terraform and Python dependencies.
#

set -euo pipefail

TERRAFORM_VERSION="1.12.1"

if ! command -v terraform >/dev/null 2>&1; then
    echo "Installing Terraform ${TERRAFORM_VERSION}"
    curl -sL "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" -o terraform.zip
    unzip terraform.zip
    mv terraform /usr/local/bin/
    rm terraform.zip
fi

echo run terraform init

terraform init


pip install -r requirements.txt
