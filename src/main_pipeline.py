import os
import pandas as pd
from google.cloud import storage
from src.utils import write_local_to_parquet, load_json, dump_columns_type_from_df
from conf.config import DATASET_EXCEL_LINKS, CONFIG_DIR, DATA_DIR
import traceback

DATASET_COLUMNS_TYPE = CONFIG_DIR.joinpath('dataset_columns_types.json')

def ingest_data_from_list_files(filename_arr_path: list):
    print("\n1. Ingestion phase")
    combined_data_df = pd.DataFrame()
    for filename_link in filename_arr_path:
        print("Getting file ", filename_link)
        data = pd.read_excel(filename_link)
        combined_data_df = pd.concat([combined_data_df, data])

    dump_columns_type_from_df(combined_data_df, filename=DATASET_COLUMNS_TYPE)

    return combined_data_df


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


def load_csv_dataset(dataset_path: str) -> pd.DataFrame:
    print(f'\n3. Loading csv dataset {dataset_path}')
    parse_dates = ['resolution']
    dataset_type = clean_type(DATASET_COLUMNS_TYPE)
    df = pd.read_csv(dataset_path, dtype=dataset_type, parse_dates=parse_dates)
    return df


def upload_to_gcs_bucket(bucket_name: str, destination_blob_name: str, source_file_name: str):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """

    # # (Ref: https://github.com/googleapis/python-storage/issues/74)

    print(f'\n5.Uploading {source_file_name} to gs://{bucket_name}/{destination_blob_name}...')
    storage_client = storage.Client()
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to gs://{bucket_name}/{destination_blob_name}.")


def end_to_end_pipeline_from_http_to_gcs(filename_arr_path: list, name_output_dataset):
    from conf.config import GCP_GCS_BUCKET
    try:
        # 1. Download excel data from links (github)
        combined_data_df = ingest_data_from_list_files(filename_arr_path)
        # 2. Convert data to csv
        path_filename_csv = save_dataset_to_csv(combined_data_df, name_output_dataset)
        # 3. Load the csv dataset freshly created
        data_df = load_csv_dataset(path_filename_csv)
        # 4. save to parquet format
        dataset_parquet_path = os.path.splitext(path_filename_csv)[0] + ".parquet"
        dataset_file_name = os.path.basename(dataset_parquet_path)
        write_local_to_parquet(data_df, dataset_parquet_path)
        # 5. Upload to GCS
        upload_to_gcs_bucket(GCP_GCS_BUCKET, dataset_file_name, dataset_parquet_path)

    except Exception as ex:
        print("Exception : ", ex)
        print(traceback.format_exc())
        exit(-1)


def end_to_end_pipeline_from_local_to_gcs(data_folder: str, name_output_dataset: str):
    from conf.config import GCP_GCS_BUCKET
    try:
        # Check before if there is CSV dataset so that we don't download again
        filename_csv = name_output_dataset + '.csv'
        path_filename_csv = DATA_DIR.joinpath(filename_csv)
        if not os.path.isfile(path_filename_csv):
            print("CSV file does not exists. Downloading")
            # 1. Get excel files from datafolder
            excel_files_path = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if file.endswith(".xlsx")]
            combined_data_df = ingest_data_from_list_files(excel_files_path)
            # 2. Convert data to csv
            path_filename_csv = save_dataset_to_csv(combined_data_df, name_output_dataset)
        else:
            print("CSV file already exists")
        # 3. Load the csv dataset freshly created
        data_df = load_csv_dataset(path_filename_csv)
        # 4. save to parquet format
        dataset_parquet_path = os.path.splitext(path_filename_csv)[0] + ".parquet"
        dataset_file_name = os.path.basename(dataset_parquet_path)
        write_local_to_parquet(data_df, dataset_parquet_path)
        # 5. Upload to GCS
        upload_to_gcs_bucket(GCP_GCS_BUCKET, dataset_file_name, dataset_parquet_path)

    except Exception as ex:
        print("Exception raised: ", ex)
        print(traceback.format_exc())
        exit(-1)


if __name__ == '__main__':
    name_output_data = "global_terrorism_db"
    local_dataset = False
    if local_dataset:
        end_to_end_pipeline_from_local_to_gcs(data_folder=DATA_DIR, name_output_dataset=name_output_data)
    else:
        end_to_end_pipeline_from_http_to_gcs(filename_arr_path=DATASET_EXCEL_LINKS,
                                             name_output_dataset=name_output_data)