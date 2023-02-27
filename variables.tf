variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default = "DEV"
}

variable "WEBSITES_PORT" {
  sensitive   = false
  default = [5000]
}

variable "URL" {
  name = "${var.prefix}.${var.URL}"
}

variable "DB_NAME" {
  sensitive   = true
  name = "${var.prefix}-${var.DB_NAME}"
}

variable "COLLECTION_NAME" {
  sensitive   = true
  name = "${var.prefix}-${var.COLLECTION_NAME}"
}

variable "FLASK_ENV" {
  sensitive   = false
}
variable "FLASK_APP" {
  sensitive   = true
}

variable "SECRET_KEY" {
  sensitive   = true
}

variable "CLIENTID" {
  sensitive   = true
}

variable "CLIENTSECRET" {
  sensitive   = true
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
