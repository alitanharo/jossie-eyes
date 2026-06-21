#!/bin/bash
# Jossie Eyes - Bicep Deployment Script
# Deploys Azure infrastructure using Bicep templates

set -e

echo "========================================="
echo "  Jossie Eyes - Deploy Azure Resources"
echo "========================================="
echo ""

# Check if Azure CLI is logged in
if ! az account show &> /dev/null; then
    echo "Error: Not logged in to Azure."
    echo "Please run ./scripts/setup_azure.sh first."
    exit 1
fi

# Set subscription (updated for new subscription)
SUBSCRIPTION_ID="3f09e186-8cc7-49d9-8c4a-79bd6acba157"
az account set --subscription $SUBSCRIPTION_ID

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
INFRA_DIR="$PROJECT_DIR/infrastructure"

echo "Project directory: $PROJECT_DIR"
echo "Infrastructure directory: $INFRA_DIR"
echo ""

# Validate Bicep file
echo "Validating Bicep template..."
bicep build "$INFRA_DIR/main.bicep"
echo "Bicep template is valid!"
echo ""

# Deploy
echo "Deploying resources to Azure..."
echo "This may take 10-15 minutes..."
echo ""

az deployment sub create \
    --location northeurope \
    --template-file "$INFRA_DIR/main.bicep" \
    --parameters location=northeurope

echo ""
echo "========================================="
echo "  Deployment complete!"
echo "========================================="
echo ""

# Get outputs
echo "Getting deployment outputs..."
DEPLOYMENT_OUTPUTS=$(az deployment sub show \
    --name main \
    --query properties.outputs \
    -o json 2>/dev/null || echo "{}")

# Extract values
RESOURCE_GROUP=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.resourceGroupName.value // empty')
AI_SERVICES_ENDPOINT=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.aiServicesEndpoint.value // empty' 2>/dev/null)
AI_SERVICES_NAME=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.aiServicesName.value // empty' 2>/dev/null)

echo ""
echo "=== Deployment Summary ==="
echo ""
echo "Resource Group: $RESOURCE_GROUP"
echo "AI Services Endpoint: $AI_SERVICES_ENDPOINT"
echo "AI Services Name: $AI_SERVICES_NAME"
echo ""
echo "Note: For GPT-4o Vision, you'll need to provide your OpenAI API key separately."
echo "Set OPENAI_API_KEY in your .env file."
echo ""

# Get keys
echo "Getting API keys..."
echo ""

# Get AI Services key
AI_SERVICES_KEY=$(az cognitiveservices account keys list \
    --name "$AI_SERVICES_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query key1 \
    -o tsv 2>/dev/null || echo "")

echo "=== API Keys ==="
echo ""
echo "AI Services Key: ${AI_SERVICES_KEY:0:10}..."
echo ""

# Create .env file
echo "Creating .env file..."
cat > "$PROJECT_DIR/.env" << EOF
# Jossie Eyes - Environment Configuration
# Generated on $(date)

# OpenAI API (for GPT-4o Vision)
# You must add your OpenAI API key manually:
# OPENAI_API_KEY=sk-your-key-here
OPENAI_API_VERSION=2024-08-01-preview

# Azure AI Services (Speech & Vision)
AZURE_SPEECH_KEY=$AI_SERVICES_KEY
AZURE_SPEECH_REGION=northeurope

# Azure Subscription
AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID
AZURE_RESOURCE_GROUP=$RESOURCE_GROUP
EOF

echo ""
echo "Environment file created at: $PROJECT_DIR/.env"
echo ""
echo "========================================="
echo "  Setup complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Review the .env file and verify the keys"
echo "2. Install Python dependencies: pip install -r requirements.txt"
echo "3. Run the edge device: python src/edge_device.py"
echo ""