output "webapp_url" {
    value = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "weba_hook" {
    value = "https://${azurerm_linux_web_app.main.site_credential[0].name}:${azurerm_linux_web_app.main.site_credential[0].password}@${azurerm_linux_web_app.main.name}.scm.azurewebsites.net/docker/hook"
    sensitive = true
}