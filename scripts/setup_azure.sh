#!/bin/bash
# Jossie Eyes - Azure Setup Script
# This script installs Azure CLI, logs in, and prepares the environment

set -e

echo "========================================="
echo "  Jossie Eyes - Azure Setup"
echo "========================================="
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Azure CLI not found. Installing..."
    
    # Install Azure CLI (Ubuntu/Debian)
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl apt-transport-https lsb-release gnupg
    
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
    
    echo "Azure CLI installed successfully!"
else
    echo "Azure CLI is already installed: $(az --version | head -n1)"
fi

# Check if Bicep is installed
if ! command -v bicep &> /dev/null; then
    echo "Bicep not found. Installing..."
    
    # Install Bicep
    AZURE_BICEP_URL="https://github.com/Azure/bicep/releases/latest/download/bicep-linux-x64"
    sudo curl -Lo /usr/local/bin/bicep $AZURE_BICEP_URL
    sudo chmod +x /usr/local/bin/bicep
    
    echo "Bicep installed successfully!"
else
    echo "Bicep is already installed: $(bicep --version | head -n1)"
fi

# Login to Azure
echo ""
echo "Please login to Azure:"
echo "You will be redirected to a browser for authentication."
echo ""

az login --use-device-code

# Set subscription
SUBSCRIPTION_ID="a070f414-2a22-4ea0-a545-565599d35f2d"
echo ""
echo "Setting subscription to: $SUBSCRIPTION_ID"
az account set --subscription $SUBSCRIPTION_ID

# Verify subscription
echo ""
echo "Current subscription:"
az account show --query "{name:name, id:id, user:user.name}"

echo ""
echo "========================================="
echo "  Azure setup complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Run ./scripts/deploy_bicep.sh to deploy Azure resources"
echo "2. Copy .env.example to .env and add your API keys"
echo "3. Run the edge device: python src/edge_device.py"
echo ""