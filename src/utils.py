import json
import pandas as pd
from pathlib import Path

def load_json(filename: str):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as ex:
        print(ex)
        exit(-1)


def write_local_to_parquet(df: pd.DataFrame, filename: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(filename)
    print(f'\n Save dataset to parquet format {path}')
    df.to_parquet(path, compression="gzip")
    print(f"File saved to {path}")
    return path

def get_excel_files_path(data_folder: Path) -> list:
    return list(data_folder.glob("**/*.xlsx"))

def read_parquet(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    return df



def dump_columns_type_from_df(df: pd.DataFrame, filename: str = 'types.json'):
    res = df.dtypes.to_frame('dtypes').reset_index()
    print("dtypes ", res)
    d = res.set_index('index')['dtypes'].astype(str).to_dict()

    with open(filename, 'w') as f:
        json.dump(d, f)

