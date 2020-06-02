locals {
  derived_cdf_name = lower(join("-", list(var.app_code, var.env)))
}

resource "google_data_fusion_instance" "instance" {
    provider                        = google-beta
    project                         = var.project_id
    name                            = local.derived_cdf_name
    description                     = var.description
    region                          = var.region
    type                            = var.type
    enable_stackdriver_logging      = var.enable_stackdriver_logging
    enable_stackdriver_monitoring   = var.enable_stackdriver_monitoring
    labels                          = var.labels
    options                         = var.options
    private_instance                = var.private_instance

    dynamic "network_config"{
        for_each = var.network_config == {} ? [] : [var.network_config]
        content{
            network             = "projects/project/global/networks/default"
            ip_allocation               = ""
    }

 }
}