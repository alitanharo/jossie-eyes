// Jossie Eyes - Azure Resources Module
// Deploys resources within the resource group
// Note: Uses OpenAI direct API for GPT-4o (no Azure OpenAI quota issues)

param location string
param resourceName string

// Azure AI Services (Multi-service account for Vision and Speech)
// This provides:
// - Computer Vision API (for image analysis)
// - Speech Service (for text-to-speech)
resource aiServices 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: '${resourceName}aiservices'
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'CognitiveServices'
  properties: {
    customSubDomainName: '${resourceName}aiservices'
    publicNetworkAccess: 'Enabled'
    apiProperties: {
      statisticsEnabled: false
    }
  }
}

// Azure AI Foundry Hub
// Provides ML experiment tracking and model management
resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: '${resourceName}aihub'
  location: location
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  kind: 'Hub'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'Jossie Eyes AI Hub'
    description: 'AI Hub for Jossie Eyes assistive device'
    publicNetworkAccess: 'Enabled'
    hbiWorkspace: false
  }
}

// Azure AI Foundry Project
// Connected to the Hub for ML operations
resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: '${resourceName}aiproject'
  location: location
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  kind: 'Project'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'Jossie Eyes AI Project'
    description: 'AI Project for Jossie Eyes assistive device'
    publicNetworkAccess: 'Enabled'
    hbiWorkspace: false
    hubResourceId: aiHub.id
  }
}

// Outputs
output aiServicesEndpoint string = aiServices.properties.endpoint
output aiServicesName string = aiServices.name
output aiHubName string = aiHub.name
output aiProjectName string = aiProject.name
