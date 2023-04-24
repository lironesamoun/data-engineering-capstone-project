import json
import pandas as pd
from pathlib import Path


def load_json(filename: str) -> json:
    """
    Load a json file
    :param filename:
    :return: json
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as ex:
        print(ex)
        exit(-1)


def write_local_to_parquet(df: pd.DataFrame, filename: str) -> Path:
    """
    Save a dataframe to parquet format
    :param df: dataframe to save to parquet
    :param filename: the output name
    :return: path where the file has been saved
    """
    """Write DataFrame out locally as parquet file"""
    path = Path(filename)
    print(f'\n Save dataset to parquet format {path}')
    df.to_parquet(path, compression="gzip")
    print(f"File saved to {path}")
    return path

def get_excel_files_path(data_folder: Path) -> list:
    """
    return in a list all the excel files found in the data_folder
    :param data_folder:
    :return:
    """
    return list(data_folder.glob("**/*.xlsx"))

def read_parquet(path: Path) -> pd.DataFrame:
    """
    Read a parquet file and return a panda dataframe
    :param path:
    :return:
    """
    df = pd.read_parquet(path)
    return df



def dump_columns_type_from_df(df: pd.DataFrame, filename: str = 'types.json'):
    """
    Given a dataframe, infer the column attributes types and save as a json
    :param df:
    :param filename:
    :return:
    """
    res = df.dtypes.to_frame('dtypes').reset_index()
    print("dtypes ", res)
    d = res.set_index('index')['dtypes'].astype(str).to_dict()

    with open(filename, 'w') as f:
        json.dump(d, f)

