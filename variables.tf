variable "LOG_LEVEL" {
  description = "Log level"
  default = "DEBUG"
  sensitive   = false
}

variable "DOCKER_REGISTRY_SERVER_URL" {
  description = "DOCKER_REGISTRY_SERVER_URL"
  default = "https://hub.docker.com/repository/registry-1.docker.io"
  sensitive   = false
}

variable "PREFIX" {
  description = "The prefix used for all resources in this environment"
  default = "dev"
  sensitive   = false
}

variable "WEBSITES_PORT" {
  description = "Website Port"
  sensitive   = false
  default = 5000
}

variable "URL_PREFIX" {
  description = "URL Prefix"
  sensitive   = false
  default = "https://"
}

variable "APP_NAME" {
  description = "URL Appname"
  sensitive   = false
  default = "app-jonl-ex12"
}

variable "URL_DOMAIN" {
  description = "URL Domain name"
  sensitive   = false
  default = "azurewebsites.net"
}

variable "FLASK_ENV" {
  description = "For Flask APP Environment"
  sensitive   = false
  default = "development"
}

variable "FLASK_APP" {
  description = "For Flask APP Entry point"
  sensitive   = false
  default = "todo_app/app"
}

variable "SECRET_KEY" {
  description = "For Flask APP"
  sensitive   = true
}

variable "DB_NAME" {
  description = "Database name"
  sensitive   = true
}

variable "COLLECTION_NAME" {
  description = "Database Collection name"
  sensitive   = true
}

variable "CLIENTID" {
  description = "Azure Service principle ID"
  sensitive   = true
}

variable "CLIENTSECRET" {
  description = "Azure Service principle secret/password"
  sensitive   = true
}

variable "LOGGLY_TOKEN" {
  description = "LOGGLY TOKEN"
  sensitive   = true
}

variable "DOCKER_REGISTRY_SERVER_PASSWORD" {
  description = "DOCKER_REGISTRY_SERVER_PASSWORD"
  sensitive   = true
}

variable "DOCKER_REGISTRY_SERVER_USERNAME" {
  description = "DOCKER_REGISTRY_SERVER_USERNAME"
  sensitive   = true
}
