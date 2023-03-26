# data-engineering-capstone-project



to do
services account IAM
Create a new service account
    BigQuery Admin
    Storage Object Admin
    Compute Storage Admin

Create and download the json key file


prefect deployment build -n "Local to GCS" -p default-agent-pool -q default-queue src/flows/flow_main_pipeline.py:ingest_csv_to_gcs --param csv_file_path="data/globalterrorismdb.csv"
prefect deployment apply ingest_csv_to_gcs-deployment.yaml
