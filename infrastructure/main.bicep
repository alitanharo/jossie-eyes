// Jossie Eyes - Azure Infrastructure
// Deploys all required Azure resources for the assistive vision device

targetScope = 'subscription'

param location string = 'northeurope'
param suffix string = uniqueString(subscription().id)
param resourceName string = 'jossieeyes${suffix}'
param openAiModelName string = 'gpt-4o'
param openAiModelVersion string = '2024-08-06'
param openAiModelFormat string = 'OpenAI'
param openAiSkuName string = 'Standard'
param openAiCapacity int = 20

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
    openAiModelName: openAiModelName
    openAiModelVersion: openAiModelVersion
    openAiModelFormat: openAiModelFormat
    openAiSkuName: openAiSkuName
    openAiCapacity: openAiCapacity
  }
}

// Outputs
output openAiEndpoint string = resources.outputs.openAiEndpoint
output openAiName string = resources.outputs.openAiName
output aiServicesEndpoint string = resources.outputs.aiServicesEndpoint
output aiServicesName string = resources.outputs.aiServicesName
output aiHubName string = resources.outputs.aiHubName
output aiProjectName string = resources.outputs.aiProjectName
output resourceGroupName string = rg.name
output location string = location
