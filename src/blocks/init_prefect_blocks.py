import json
import os
from dotenv import load_dotenv
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect.filesystems import GitHub

load_dotenv()

bucket_name_GCS = os.environ.get("TF_VAR_GCP_GCS_BUCKET")
BASELINE_BLOCK_NAME = "capstone-project-gcs"
BLOCK_NAME_CREDENTIALS = f"{BASELINE_BLOCK_NAME}-credentials"
BLOCK_NAME_BUCKET = f"{BASELINE_BLOCK_NAME}-bucket"
BLOCK_NAME_GITHUB = f"{BASELINE_BLOCK_NAME}-github"


def create_credentials_block():
    """
    Create the GCP credentials blocks for Prefect
    :return:
    """
    with open(os.environ.get("GCP_CREDENTIALS_PREFECT_SERVICE_ACCOUNT")) as prefect_service_account_file:
        prefect_service_account = prefect_service_account_file.read()

    credentials_block = GcpCredentials(
        service_account_info=json.loads(prefect_service_account)  # (2) enter your credentials info here
    )

    credentials_block.save(BLOCK_NAME_CREDENTIALS, overwrite=True)


def create_gcs_bucket_block():
    """
    Create the google cloud bucket blocks for prefect
    :return:
    """
    bucket_block = GcsBucket(
        gcp_credentials=GcpCredentials.load(BLOCK_NAME_CREDENTIALS),
        bucket=f"{bucket_name_GCS}",
    )

    bucket_block.save(BLOCK_NAME_BUCKET, overwrite=True)


def create_github_block():
    """
    Create the github blocks for prefect
    :return:
    """
    github_block = GitHub(
        repository=os.getenv('GITHUB_REPOSITORY_URL'),
        access_token=os.getenv('GITHUB_REPO_ACCESS_TOKEN')
    )
    github_block.save(BLOCK_NAME_GITHUB, overwrite=True)


if __name__ == '__main__':
    create_credentials_block()
    create_gcs_bucket_block()
    create_github_block()
