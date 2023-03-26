import json
import os

import pandas as pd

from conf.config import CONFIG_DIR, DATA_DIR


def dump_type_from_df(df: pd.DataFrame, filename: str = 'types.json'):
    res = df.dtypes.to_frame('dtypes').reset_index()
    d = res.set_index('index')['dtypes'].astype(str).to_dict()

    with open(filename, 'w') as f:
        json.dump(d, f)


def init_dataset(folder_path: str = DATA_DIR, name_dataset: str = "globalterrorismdb"):
    excel_files = [file for file in os.listdir(folder_path) if file.endswith(".xlsx")]

    combined_data = pd.DataFrame()

    for excel_file in excel_files:
        print(f"Processing {excel_file}")
        file_path = os.path.join(folder_path, excel_file)
        data = pd.read_excel(file_path)
        combined_data = pd.concat([combined_data, data])


    dump_type_from_df(combined_data, filename=CONFIG_DIR.joinpath('dataset_types.json'))
    # save the combined data to a CSV file
    combined_data.to_csv(DATA_DIR.joinpath(name_dataset+'.csv'), index=False)


if __name__ == '__main__':

    init_dataset(DATA_DIR, name_dataset="globalterrorismdb")
