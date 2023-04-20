locals {
  data_lake_bucket = "global-terrorism-data-bucket"
}

variable "GCP_CREDS" {
  description = "Credentials for GCP"
  type        = string
}

variable "GCP_PROJECT_ID" {
  description = "Project id"
  default     = "de-capstone-project-23"
  type        = string
}

variable "GCP_REGION" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  type        = string
  default     = "europe-west3"
}

variable "GCP_STORAGE_CLASS" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}

variable "GCP_BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
}