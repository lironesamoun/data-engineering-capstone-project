import os
import traceback
from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect_gcp import GcpCredentials, GcsBucket

from conf.config import CONFIG_DIR, DATA_DIR, DATASET_EXCEL_LINKS, GCP_BIGQUERY_DESTINATION_TABLE, GCLOUD_PROJECT
from src.blocks.init_prefect_blocks import BLOCK_NAME_BUCKET
from src.utils import dump_columns_type_from_df, load_json, write_local_to_parquet, get_excel_files_path

DATASET_COLUMNS_TYPE = CONFIG_DIR.joinpath('dataset_columns_types.json')

@task(name="ingest_data_from_list_files",
      description="Given a list of path (link or local), ingest data, "
                  "create a combined dataframe, infer types and return a combined dataframe")
def ingest_data_from_list_files(filename_arr_path: list):
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
    print(f'\n2. Saving dataset to csv {name_output_dataset}')
    # save the combined data to a CSV file
    filename_csv = name_output_dataset + '.csv'
    path_filename_csv = DATA_DIR.joinpath(filename_csv)
    df.to_csv(path_filename_csv, index=False)
    return path_filename_csv


def clean_type(dataset_type: str):
    dataset_type = load_json(dataset_type)
    dataset_type.pop('resolution')

    return dataset_type


@task(name="load_dataset",
      description="Load the dataset in csv format, clean type ")
def load_csv_dataset(dataset_path: str) -> pd.DataFrame:
    print(f'\n3. Loading csv dataset {dataset_path}')
    parse_dates = ['resolution']
    dataset_type = clean_type(DATASET_COLUMNS_TYPE)
    df = pd.read_csv(dataset_path, dtype=dataset_type, parse_dates=parse_dates)
    return df


@task(name="upload to gcs bucket",
      description="Upload a parquet file to Google Cloud Storage")
def upload_to_gcs_bucket(source_file_name: str):
    print(f'\n5.Uploading {source_file_name} to GCS bucket')
    gcs_block = GcsBucket.load("capstone-project-gcs-bucket")
    gcs_block.upload_from_path(from_path=source_file_name, timeout=500)


@task(retries=3)
def extract_from_gcs_to_local(filename: str) -> Path:
    """Download data from GCS"""
    print(f'\n6.Extract data {filename} from GCS bucket')
    gcs_path = f"{filename}"
    gcs_block = GcsBucket.load(BLOCK_NAME_BUCKET)
    #Copies a folder from the configured GCS bucket to a local directory
    gcs_block.get_directory(from_path=gcs_path, local_path=DATA_DIR)
    return Path(f"{DATA_DIR}/{gcs_path}")

@task(name="write_data_google_bq",
      description="Upload the parquet file data to Google Big query")
def write_data_google_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("capstone-project-gcs-credentials")

    df.to_gbq(
        destination_table=GCP_BIGQUERY_DESTINATION_TABLE,
        project_id=GCLOUD_PROJECT,
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )
    print("Successfully uploaded data to BigQuery.")


@flow(name="end_to_end_pipeline_from_http_to_bq",
      description="Flow that download the dataset in excel format given a list of links (excel), "
                  "Combine the data, save it to csv, convert to parquet and then upload to google cloud bucket",
      log_prints=True)
def end_to_end_pipeline_from_http_to_bq(filename_arr_path: list, name_output_dataset):
    from conf.config import GCP_GCS_BUCKET
    try:
        # 0. Check beforehand if there is CSV dataset so that we don't download again
        filename_csv = name_output_dataset + '.csv'
        path_filename_csv = DATA_DIR.joinpath(filename_csv)
        if not os.path.isfile(path_filename_csv):
            # 1. Download excel data from links (github)
            combined_data_df = ingest_data_from_list_files(filename_arr_path)
            # 2. Convert data to csv
            path_filename_csv = save_dataset_to_csv(combined_data_df, name_output_dataset)
        else:
            print("CSV file already exists")
        # 3. Load the csv dataset freshly created
        data_df = load_csv_dataset(path_filename_csv)
        # 4. save to parquet format
        dataset_parquet_path = os.path.splitext(path_filename_csv)[0] + ".parquet"
        write_local_to_parquet(data_df, dataset_parquet_path)
        # 5. Upload to GCS
        upload_to_gcs_bucket(dataset_parquet_path)
        # 6. Upload to Google Big query
        write_data_google_bq(data_df)

    except Exception as ex:
        print("Exception raised: ", ex)
        print(traceback.format_exc())
        exit(-1)

@flow(name="end_to_end_pipeline_from_local_to_bq",
      description="Flow that take the dataset in excel format given a list of links inside a specific folder, "
                  "Combine the data, save it to csv, convert to parquet and then upload to google cloud bucket",
      log_prints=True)
def end_to_end_pipeline_from_local_to_bq(data_folder: Path, name_output_dataset: str):
    from conf.config import GCP_GCS_BUCKET
    try:
        #0. Check beforehand if there is CSV dataset so that we don't download again
        filename_csv = name_output_dataset + '.csv'
        path_filename_csv = DATA_DIR.joinpath(filename_csv)
        if not os.path.isfile(path_filename_csv):
            print("CSV file does not exists. Downloading")
            # 1. Get excel files from datafolder
            excel_files_path = get_excel_files_path(data_folder)
            combined_data_df = ingest_data_from_list_files(excel_files_path)
            # 2. Convert data to csv
            path_filename_csv = save_dataset_to_csv(combined_data_df, name_output_dataset)
        else:
            print("CSV file already exists")
        # 3. Load the csv dataset freshly created
        data_df = load_csv_dataset(path_filename_csv)
        # 4. save to parquet format
        dataset_parquet_path = os.path.splitext(path_filename_csv)[0] + ".parquet"
        write_local_to_parquet(data_df, dataset_parquet_path)
        # 5. Upload to GCS
        upload_to_gcs_bucket(dataset_parquet_path)
        # 6. Upload to Google Big query
        write_data_google_bq(data_df)

    except Exception as ex:
        print("Exception raised: ", ex)
        print(traceback.format_exc())
        exit(-1)


if __name__ == '__main__':
    name_output_data = "global_terrorism_db"
    local_dataset = True
    if local_dataset:
        end_to_end_pipeline_from_local_to_bq(data_folder=DATA_DIR, name_output_dataset=name_output_data)
    else:
        end_to_end_pipeline_from_http_to_bq(filename_arr_path=DATASET_EXCEL_LINKS,
                                             name_output_dataset=name_output_data)