// Jossie Eyes - Azure Resources Module
// Deploys resources within the resource group

param location string
param resourceName string
param openAiModelName string
param openAiModelVersion string
param openAiModelFormat string
param openAiSkuName string
param openAiCapacity int

// Azure OpenAI Service
resource openai 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: '${resourceName}openai'
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'OpenAI'
  properties: {
    customSubDomainName: '${resourceName}openai'
    publicNetworkAccess: 'Enabled'
  }
}

// GPT-4o Model Deployment
resource gpt4oDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openai
  name: openAiModelName
  sku: {
    name: openAiSkuName
    capacity: openAiCapacity
  }
  properties: {
    model: {
      format: openAiModelFormat
      name: openAiModelName
      version: openAiModelVersion
    }
  }
}

// Azure AI Services (Multi-service account for Vision and Speech)
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
  dependsOn: [
    aiHub
  ]
}

// Outputs
output openAiEndpoint string = openai.properties.endpoint
output openAiName string = openai.name
output aiServicesEndpoint string = aiServices.properties.endpoint
output aiServicesName string = aiServices.name
output aiHubName string = aiHub.name
output aiProjectName string = aiProject.name
