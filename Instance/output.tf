output "cdf_instance" {
  value = google_data_fusion_instance.instance
  description = "The created CDF instance details"
}

locals {
  tenant_project_re = "cloud-data-fusion-management-sa@([\\w-]+).iamgserviceaccount.com"
}

output "tenant_project_re" {
  value = regex(local.tenant_project_re, google_data_fusion_instance.instance.service_account)[0]
  description = "This google managed tenant projec id in which cdf is created"
}

