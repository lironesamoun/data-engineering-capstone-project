from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from conf.config import DATA_DIR


@task(retries=3)
def extract_from_gcs(filename: str) -> Path:
    """Download data from GCS"""
    gcs_path = f"{filename}"
    gcs_block = GcsBucket.load("capstone-project-gcs-bucket")
    gcs_block.get_directory(from_path=gcs_path, local_path=DATA_DIR)
    return Path(f"{DATA_DIR}/{gcs_path}")


@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("capstone-project-gcs-credentials")

    df.to_gbq(
        destination_table="globalterrorism_raw.data",
        project_id="de-capstone-project-23",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )
    print("Successfully uploaded data to BigQuery.")

@flow()
def etl_gcs_to_bq(filename_on_gcs: str):
    path = extract_from_gcs(filename_on_gcs)
    df = transform(path)
    write_bq(df)

if __name__ == '__main__':
    etl_gcs_to_bq(filename_on_gcs="globalterrorismdb.parquet")