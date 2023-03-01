variable "PREFIX" {
  description = "The prefix used for all resources in this environment"
  default = "dev"
  sensitive   = false
}

variable "WEBSITES_PORT" {
  sensitive   = false
  default = 5000
}

variable "URL_PREFIX" {
    sensitive   = false
    default = "https://"
}

variable "URL_DOMAIN" {
    sensitive   = false
    default = "azurewebsites.net"
}

variable "APP_NAME" {
    sensitive   = false
    default = "app-jonl-ex12"
}

variable "DB_NAME" {
  sensitive   = true
}

variable "FLASK_ENV" {
  sensitive   = false
  default = "development"
}

variable "FLASK_APP" {
  sensitive   = false
  default = "todo_app/app"
}

variable "SECRET_KEY" {
  sensitive   = true
}
variable "COLLECTION_NAME" {
  sensitive   = true
}

variable "CLIENTID" {
  sensitive   = true
}

variable "CLIENTSECRET" {
  sensitive   = true
}

variable "TF_VAR_CLIENT_ID" {
  sensitive   = true
}
variable "TF_VAR_CLIENT_SECRET" {
  sensitive   = true
}
variable "TF_VAR_TENANT_ID" {
  sensitive   = true
}
variable "TF_VAR_SUBSCRIPTION_ID" {
  sensitive   = true
}
