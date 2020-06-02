
variable "app_code" {
    description = "App Code"
    type = string
}

variable "env" {
    description = "Enviornment"
    type = string
}

variable "description"{
    description = "an optional description of the isntance"
    type = string
    default = ""
}

variable "region" {
    description = "The region of the data fusion instance"
    type = string
}

variable "type" {
    description = "Repressents the tyoe if data fusion instance (BASIC or ENTERPRISE)"
    type = string
    default = "BASIC"  
}
variable "enable_stackdriver_logging" {
    description = "Option to enable stackdriver logging"
    type = bool
    default = true
}

variable "enable_stackdriver_monitoring" {
    description = "option to enable stackdriver monitoring"
    type = bool
    default = true
}

variable "labels" {
    description = "the resource labels for instance to use the annotate any related underlying resource, such as compute engine VMs"
    type = map(string)
    default = {}  
}

variable "options" {
    description = "map of additional options used to configure the behavior of the data fusion instance"
    type = map(string)
    default = {}
}

variable "private_instance" {
    description = "specifies whether the data fusion insatnce should be private. if set to true, all data fusion nodes will have a private IP address and will not be able to access external internet"
    type = bool
    default = false
}

variable "network_config" {
    description = "network configuration options. these are required when a private data fusion instance is to be created"
    type = map(string)
    default = {}
}

variable "project_id" {
    description = "project id for CDF"
    type = string
}















