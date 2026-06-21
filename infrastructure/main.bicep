// Jossie Eyes - Azure Infrastructure
// Deploys Azure AI Services, AI Foundry Hub & Project
// Note: Uses OpenAI direct API for GPT-4o (no Azure OpenAI quota issues)

targetScope = 'subscription'

param location string = 'northeurope'
param suffix string = uniqueString(subscription().id)
param resourceName string = 'jossieeyes${suffix}'

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-jossie-eyes'
  location: location
}

// Module for resources within the resource group
module resources './resources.bicep' = {
  name: 'jossie-eyes-resources'
  scope: rg
  params: {
    location: location
    resourceName: resourceName
  }
}

// Outputs
output aiServicesEndpoint string = resources.outputs.aiServicesEndpoint
output aiServicesName string = resources.outputs.aiServicesName
output aiHubName string = resources.outputs.aiHubName
output aiProjectName string = resources.outputs.aiProjectName
output resourceGroupName string = rg.name
output location string = location
