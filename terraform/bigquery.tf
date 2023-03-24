# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.GCP_BQ_DATASET
  project    = var.GCP_PROJECT_ID
  location   = var.GCP_REGION
}