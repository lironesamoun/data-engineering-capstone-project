import os
import pandas as pd
from prefect import task
from prefect_gcp import GcpCredentials, GcsBucket

from conf.config import CONFIG_DIR, DATA_DIR
from src.blocks.init_prefect_blocks import BLOCK_NAME_BUCKET, BLOCK_NAME_CREDENTIALS
from src.utils import dump_columns_type_from_df, load_json
from dotenv import load_dotenv

DATASET_COLUMNS_TYPE = CONFIG_DIR.joinpath('dataset_columns_types.json')

@task(name="ingest_data_from_list_files",
      description="Given a list of path (link or local), ingest data, "
                  "create a combined dataframe, infer types and return a combined dataframe")
def ingest_data_from_list_files(filename_arr_path: list):
    """
    Given a list of file path, load the data, create a combined dataframe
    :param filename_arr_path:
    :return:
    """
    print("\n1. Ingestion phase")
    combined_data_df = pd.DataFrame()
    for filename_link in filename_arr_path:
        print("Getting file ", filename_link)
        data = pd.read_excel(filename_link)
        combined_data_df = pd.concat([combined_data_df, data])

    dump_columns_type_from_df(combined_data_df, filename=DATASET_COLUMNS_TYPE)

    return combined_data_df


@task(name="save_dataset_to_csv",
      description="Given a dataframe, save the dataset to csv")
def save_dataset_to_csv(df: pd.DataFrame, name_output_dataset: str = "globalterrorismdb"):
    """
    Save a dataframe to csv
    :param df:
    :param name_output_dataset:
    :return:
    """
    print(f'\n2. Saving dataset to csv {name_output_dataset}')
    # save the combined data to a CSV file
    filename_csv = name_output_dataset + '.csv'
    path_filename_csv = DATA_DIR.joinpath(filename_csv)
    df.to_csv(path_filename_csv, index=False)
    return path_filename_csv


def clean_type(dataset_type: str):
    """
    given the json file that contain all the columns types of the dataset, remove the one that we don't want to use
    :param dataset_type:
    :return:
    """
    if not os.path.isfile(dataset_type):
        raise FileNotFoundError

    dataset_type = load_json(dataset_type)
    dataset_type.pop('resolution')

    return dataset_type


@task(name="load_dataset",
      description="Load the dataset in csv format, clean type ")
def load_csv_dataset(dataset_path: str) -> pd.DataFrame:
    """
    Load CSV data
    :param dataset_path:
    :return:
    """
    print(f'\n3. Loading csv dataset {dataset_path}')
    parse_dates = ['resolution']
    dataset_type = clean_type(DATASET_COLUMNS_TYPE)
    df = pd.read_csv(dataset_path, dtype=dataset_type, parse_dates=parse_dates)
    return df


@task(name="upload to gcs bucket",
      description="Upload a parquet file to Google Cloud Storage")
def upload_to_gcs_bucket(source_file_name: str):
    """
    Upload data to google cloud bucket
    :param source_file_name:
    :return:
    """
    print(f'\n5.Uploading {source_file_name} to GCS bucket')
    gcs_block = GcsBucket.load(BLOCK_NAME_BUCKET)
    gcs_block.upload_from_path(from_path=source_file_name, timeout=500)


@task(retries=3)
def extract_from_gcs_to_local(filename: str) -> pd.DataFrame:
    """Download data from GCS"""
    print(f'\n6.Extract data {filename} from GCS bucket')
    gcs_path = f"{filename}"
    gcs_block = GcsBucket.load(BLOCK_NAME_BUCKET)
    #Copies a folder from the configured GCS bucket to a local directory
    gcs_block.get_directory(from_path=gcs_path, local_path=DATA_DIR)
    df = pd.read_parquet(f"{DATA_DIR}/{gcs_path}")
    return df


@task(name="write_data_google_bq",
      description="Upload the parquet file data to Google Big query")
def write_data_google_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""
    load_dotenv()

    gcp_credentials_block = GcpCredentials.load(BLOCK_NAME_CREDENTIALS)

    df.to_gbq(
        destination_table=os.environ.get("GCP_BIGQUERY_DESTINATION_TABLE"),
        project_id=os.environ.get("TF_VAR_GCP_PROJECT_ID"),
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
        location=os.environ.get("TF_VAR_GCP_REGION")
    )
    print("Successfully uploaded data to BigQuery.")

