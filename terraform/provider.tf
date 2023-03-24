
provider "google" {
  project = var.GCP_PROJECT_ID
  region  = var.GCP_REGION
  #credentials = file(var.gcp-creds)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}




