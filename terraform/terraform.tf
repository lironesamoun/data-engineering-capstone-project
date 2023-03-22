
provider "google" {
  project = var.GCP_PROJECT_ID
  region  = var.GCP_REGION
  #credentials = file(var.gcp-creds)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name     = local.data_lake_bucket # Concatenating DL bucket & Project name for unique naming
  location = var.GCP_REGION

  # Optional, but recommended settings:
  storage_class               = var.GCP_STORAGE_CLASS
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}


# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.GCP_BQ_DATASET
  project    = var.GCP_PROJECT_ID
  location   = var.GCP_REGION
}