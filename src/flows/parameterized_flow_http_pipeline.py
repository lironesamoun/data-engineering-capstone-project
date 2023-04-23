import os
import traceback
from prefect import flow
from conf.config import DATA_DIR, DATASET_EXCEL_LINKS
from src.utils import write_local_to_parquet
from src.flows.pipeline_components import ingest_data_from_list_files, load_csv_dataset, save_dataset_to_csv, upload_to_gcs_bucket, write_data_google_bq


@flow(name="end_to_end_pipeline_from_http_to_bq",
      description="Flow that download the dataset in excel format given a list of links (excel), "
                  "Combine the data, save it to csv, convert to parquet and then upload to google cloud bucket",
      log_prints=True)
def end_to_end_pipeline_from_http_to_bq(filename_arr_path: list = DATASET_EXCEL_LINKS,
                                        name_output_dataset="global_terrorism_db"):
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


if __name__ == '__main__':
    name_output_data = "global_terrorism_db"
    filename_arr_path = DATASET_EXCEL_LINKS
    end_to_end_pipeline_from_http_to_bq(filename_arr_path=DATASET_EXCEL_LINKS, name_output_dataset=name_output_data)
