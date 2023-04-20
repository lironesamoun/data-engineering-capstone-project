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
BASELINE_BLOCK_NAME = "capstone-project-gcs"
BLOCK_NAME_CREDENTIALS = f"{BASELINE_BLOCK_NAME}-credentials"
BLOCK_NAME_BUCKET = f"{BASELINE_BLOCK_NAME}-bucket"
BLOCK_NAME_GITHUB = f"{BASELINE_BLOCK_NAME}-github"


def create_credentials_block():
    with open(os.environ.get("PREFECT_SERVICE_ACCOUNT")) as prefect_service_account_file:
        prefect_service_account = prefect_service_account_file.read()

    credentials_block = GcpCredentials(
        service_account_info=json.loads(prefect_service_account)  # (2) enter your credentials info here
    )

    credentials_block.save(BLOCK_NAME_CREDENTIALS, overwrite=True)


def create_gcs_bucket_block():
    bucket_block = GcsBucket(
        gcp_credentials=GcpCredentials.load(BLOCK_NAME_CREDENTIALS),
        bucket=f"{bucket_name_GCS}",
    )

    bucket_block.save(BLOCK_NAME_BUCKET, overwrite=True)


def create_github_block():
    github_block = GitHub(
        repository=os.getenv('GITHUB_REPOSITORY_URL'),
        access_token=os.getenv('GITHUB_REPO_ACCESS_TOKEN')
    )
    github_block.save(BLOCK_NAME_GITHUB, overwrite=True)


if __name__ == '__main__':
    create_credentials_block()
    create_gcs_bucket_block()
    create_github_block()
