variable "yc_token" {
  type        = string
  description = "OAuth token for Yandex Cloud"
  sensitive   = true
}

variable "yc_cloud_id" {
  type        = string
  description = "ID of the cloud"
}

variable "yc_folder_id" {
  type        = string
  description = "ID of the folder"
}