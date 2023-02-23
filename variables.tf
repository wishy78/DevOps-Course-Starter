variable "FLASK_APP" {
  sensitive   = true
}

variable "FLASK_ENV" {
  sensitive   = false
}

variable "SECRET_KEY" {
  sensitive   = true
}

variable "DB_NAME" {
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

variable "WEBSITES_PORT" {
  sensitive   = false
}

variable "DOCKER_REGISTRY_SERVER_URL" {
  sensitive   = true
}

variable "DOCKER_REGISTRY_SERVER_PASSWORD" {
  sensitive   = true
}

variable "DOCKER_REGISTRY_SERVER_USERNAME" {
  sensitive   = true
}
