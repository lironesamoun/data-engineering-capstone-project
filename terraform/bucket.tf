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