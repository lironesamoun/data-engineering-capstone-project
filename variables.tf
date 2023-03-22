locals {
  data_lake_bucket = "global-terrorism-data"
}

variable "gcp-creds" {
  description = "Credentials for GCP"
  default     = "europe-west3"
  type        = string
}

variable "project" {
  description = "de-capstone-project-23"
  default     = "de-capstone-project-23"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "europe-west3"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "global_terrorism_data"
}