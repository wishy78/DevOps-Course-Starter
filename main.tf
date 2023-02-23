terraform {
    required_providers {
        azurerm = {
        source = "hashicorp/azurerm"
        version = ">= 3.8"
        }
    }
}

provider "azurerm" {
    features {}
}

data "azurerm_resource_group" "main" {
    name = "Cohort22_JonLon_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name = "terraformed-mod12-asp"
  location = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type = "Linux"
  sku_name = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name = "APP-JonL-Ex12"
  location = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id = azurerm_service_plan.main.id
  
  site_config {
    application_stack {
      docker_image = "wishy78/todo-app"
      docker_image_tag = "latest"
    }
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGODB_CONNECTION_STRING" = azurerm_cosmosdb_account.db.connection_strings[0]
    
  }
}

resource "azurerm_cosmosdb_account" "db" {
  name                = "cosmos-to-do-mod12-jl"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = true

  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }
  
  capabilities { 
    name = "EnableServerless" 
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "collection" {
  name                = "to-do-list"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.db.name
  throughput          = 400
}



 
 