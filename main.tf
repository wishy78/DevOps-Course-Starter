terraform {
    required_providers {
        azurerm = {
          source = "hashicorp/azurerm"
          version = ">= 3.8"
        }
    }
    backend "azurerm" {
        resource_group_name  = "Cohort22_JonLon_ProjectExercise"
        storage_account_name = "tfstate1147207684"
        container_name       = "tfstate"
        key                  = "$env:ARM_ACCESS_KEY"
    }
}

provider "azurerm" {
    features {}
# ARM_ environmets are use from Pipeline to login automatically
}

data "azurerm_resource_group" "main" {
    name = "Cohort22_JonLon_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name = "${var.PREFIX}-terraformed-asp"
  location = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type = "Linux"
  sku_name = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name = "${var.PREFIX}-${var.APP_NAME}"
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
    "FLASK_APP" = var.FLASK_APP
    "FLASK_ENV" = "${var.FLASK_ENV}"
    "SECRET_KEY"="${var.SECRET_KEY}"

    "CON_STRING"="${azurerm_cosmosdb_account.dbServer.connection_strings[0]}"
    "DB_NAME"="${var.DB_NAME}"
    "COLLECTION_NAME"="${var.COLLECTION_NAME}"
 
    "CLIENTID"="${var.CLIENTID}"
    "CLIENTSECRET"="${var.CLIENTSECRET}"
    "URL"="${var.URL_PREFIX}${var.PREFIX}-${var.APP_NAME}.${var.URL_DOMAIN}"

    "WEBSITES_PORT" = "${var.WEBSITES_PORT}"
  }
}

resource "azurerm_cosmosdb_account" "dbServer" {
  name                = "${var.DB_NAME}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"
  
  lifecycle { 
    prevent_destroy = true 
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

resource "azurerm_cosmosdb_mongo_database" "DB" {
  name                = "${var.COLLECTION_NAME}"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.dbServer.name
}
