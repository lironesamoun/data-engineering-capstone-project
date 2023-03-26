from prefect_gcp import GcsBucket
from prefect import flow, task
import os
import pandas as pd
from src.utils import write_local, load_json
import traceback


def clean_type(dataset_type: str):
    dataset_type = load_json(dataset_type)
    dataset_type.pop('resolution')

    return dataset_type


@task(name="load_dataset",
      description="Load the Global Terrorism dataset")
def load_dataset(dataset_path: str) -> pd.DataFrame:
    print("Loading dataset ", dataset_path)
    parse_dates = ['resolution']
    dataset_type = clean_type("conf/dataset_types.json")
    df = pd.read_csv(dataset_path, dtype=dataset_type, parse_dates=parse_dates)
    return df


@task(name="upload to gcs bucket",
      description="Upload a parquet file to Google Cloud Storage")
def upload_to_gcs_bucket(source_file_name: str):

    gcs_block = GcsBucket.load("capstone-project-gcs-bucket")
    gcs_block.upload_from_path(from_path=source_file_name)
    print(f"File {source_file_name} uploaded to GCS bucket")


@flow(name="Global Terrorism Dataset to GSC",
      description="Flow that take a CSV file and upload it to Google Cloud Storage",
      log_prints=True)
def ingest_csv_to_gcs(csv_file_path: str):
    try:
        print(f"Processing {csv_file_path}")
        dataset_df = load_dataset(csv_file_path)
        dataset_parquet_path = os.path.splitext(csv_file_path)[0] + ".parquet"
        write_local(dataset_df, dataset_parquet_path)

        upload_to_gcs_bucket(dataset_parquet_path)

    except Exception as ex:
        print("Exception : ", ex)
        print(traceback.format_exc())
        exit(-1)


if __name__ == '__main__':
    ingest_csv_to_gcs("data/globalterrorismdb.csv")