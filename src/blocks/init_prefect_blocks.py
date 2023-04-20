import json
import os

from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect.filesystems import GitHub

from conf.config import GCP_GCS_BUCKET

# This is an alternative to creating GCP blocks in the UI
# (1) insert your own GCS bucket name
# (2) insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!

bucket_name_GCS = GCP_GCS_BUCKET  # (1) insert your GCS bucket name
baseline_block_name = "capstone-project-gcs"
block_name_credentials = f"{baseline_block_name}-credentials"
block_name_bucket = f"{baseline_block_name}-bucket"
block_name_github = f"{baseline_block_name}-github"


def create_credentials_block():
    with open(os.environ.get("PREFECT_SERVICE_ACCOUNT")) as prefect_service_account_file:
        prefect_service_account = prefect_service_account_file.read()

    credentials_block = GcpCredentials(
        service_account_info=json.loads(prefect_service_account)  # (2) enter your credentials info here
    )

    credentials_block.save(block_name_credentials, overwrite=True)


def create_gcs_bucket_block():
    bucket_block = GcsBucket(
        gcp_credentials=GcpCredentials.load(block_name_credentials),
        bucket=f"{bucket_name_GCS}",
    )

    bucket_block.save(block_name_bucket, overwrite=True)


def create_github_block():
    github_block = GitHub(
        repository=os.getenv('GITHUB_REPOSITORY_URL'),
        access_token=os.getenv('GITHUB_REPO_ACCESS_TOKEN')
    )
    github_block.save(block_name_github, overwrite=True)


if __name__ == '__main__':
    create_credentials_block()
    create_gcs_bucket_block()
    create_github_block()
