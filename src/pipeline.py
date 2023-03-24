import os
import pandas as pd
from google.cloud import storage
from src.utils import write_local, load_json
import traceback

def clean_type(dataset_type: str):
    dataset_type = load_json(dataset_type)
    dataset_type.pop('resolution')

    return dataset_type


def load_dataset(dataset_path: str) -> pd.DataFrame:
    print("Loading dataset ", dataset_path)
    parse_dates = ['resolution']
    dataset_type = clean_type("conf/dataset_types.json")
    df = pd.read_csv(dataset_path, dtype=dataset_type, parse_dates=parse_dates)
    return df

def upload_to_gcs_bucket(bucket_name: str, destination_blob_name: str, source_file_name: str):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    print(f"Uploading {source_file_name} to gs://{bucket_name}/{destination_blob_name}...")
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to gs://{bucket_name}/{destination_blob_name}.")


def ingest_csv_to_gcs(csv_file_path: str):
    from conf.config import GCP_GCS_BUCKET
    try:
        print(f"Processing {csv_file_path}")
        dataset_df = load_dataset(csv_file_path)
        dataset_parquet_path = os.path.splitext(csv_file_path)[0] + ".parquet"
        dataset_file_name = os.path.basename(dataset_parquet_path)
        write_local(dataset_df, dataset_parquet_path)

        upload_to_gcs_bucket(GCP_GCS_BUCKET, dataset_file_name, dataset_parquet_path)

    except Exception as ex:
        print("Exception : ", ex)
        print(traceback.format_exc())
        exit(-1)

if __name__ == '__main__':
    ingest_csv_to_gcs("data/globalterrorismdb.csv")