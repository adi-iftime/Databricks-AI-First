// Azure stack: Databricks access connector + workspace + ADLS Gen2 + UC metastore container.
// Deploy with: az deployment group create -g <rg> -f infra/main.bicep --parameters ...

@description('Azure region for all resources')
param location string = 'northeurope'

@description('Databricks workspace name')
param workspaces_adb_cursorfun_dev_name string = 'adb-cursorfun-dev'

@description('Storage account name (globally unique, lowercase alphanumeric)')
param storageAccounts_stcursorfundevne_name string = 'stcursorfundevne'

@description('Databricks access connector name')
param accessConnectors_ac_cursorfun_dev_name string = 'ac-cursorfun-dev'

@description('Principal ID for workspace authorizations (e.g. Unity Catalog / connector identity). Leave empty to omit authorizations.')
param workspaceAuthorizationPrincipalId string = ''

@description('Azure RBAC role definition ID for the authorization entry (default: Owner)')
param workspaceAuthorizationRoleDefinitionId string = '8e3af657-a8ff-443c-a75c-2fe8c4bcb635'

resource accessConnector 'Microsoft.Databricks/accessConnectors@2026-01-01' = {
  name: accessConnectors_ac_cursorfun_dev_name
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}
}

resource workspace 'Microsoft.Databricks/workspaces@2026-01-01' = {
  name: workspaces_adb_cursorfun_dev_name
  location: location
  sku: {
    name: 'premium'
  }
  properties: {
    computeMode: 'Serverless'
    publicNetworkAccess: 'Enabled'
    authorizations: !empty(workspaceAuthorizationPrincipalId)
      ? [
          {
            principalId: workspaceAuthorizationPrincipalId
            roleDefinitionId: workspaceAuthorizationRoleDefinitionId
          }
        ]
      : []
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2025-06-01' = {
  name: storageAccounts_stcursorfundevne_name
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    dualStackEndpointPreference: {
      publishIpv6Endpoint: false
    }
    dnsEndpointType: 'Standard'
    defaultToOAuthAuthentication: false
    publicNetworkAccess: 'Enabled'
    allowCrossTenantReplication: false
    isSftpEnabled: false
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: true
    isHnsEnabled: true
    networkAcls: {
      ipv6Rules: []
      bypass: 'AzureServices'
      virtualNetworkRules: []
      ipRules: []
      defaultAction: 'Allow'
    }
    supportsHttpsTrafficOnly: true
    encryption: {
      requireInfrastructureEncryption: false
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    accessTier: 'Hot'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2025-06-01' = {
  parent: storage
  name: 'default'
  properties: {
    containerDeleteRetentionPolicy: {
      enabled: true
      days: 7
    }
    cors: {
      corsRules: []
    }
    deleteRetentionPolicy: {
      allowPermanentDelete: false
      enabled: true
      days: 7
    }
  }
}

resource fileService 'Microsoft.Storage/storageAccounts/fileServices@2025-06-01' = {
  parent: storage
  name: 'default'
  properties: {
    protocolSettings: {
      smb: {
        encryptionInTransit: {
          required: true
        }
      }
    }
    cors: {
      corsRules: []
    }
    shareDeleteRetentionPolicy: {
      enabled: true
      days: 7
    }
  }
}

resource queueService 'Microsoft.Storage/storageAccounts/queueServices@2025-06-01' = {
  parent: storage
  name: 'default'
  properties: {
    cors: {
      corsRules: []
    }
  }
}

resource tableService 'Microsoft.Storage/storageAccounts/tableServices@2025-06-01' = {
  parent: storage
  name: 'default'
  properties: {
    cors: {
      corsRules: []
    }
  }
}

resource ucMetastoreContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2025-06-01' = {
  parent: blobService
  name: 'uc-metastore-cursorfun-northeurope'
  properties: {
    immutableStorageWithVersioning: {
      enabled: false
    }
    defaultEncryptionScope: '$account-encryption-key'
    denyEncryptionScopeOverride: false
    publicAccess: 'None'
  }
}

output workspaceId string = workspace.id
output storageAccountId string = storage.id
output accessConnectorId string = accessConnector.id
output accessConnectorPrincipalId string = accessConnector.identity.principalId
