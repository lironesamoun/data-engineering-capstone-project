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


def write_local(df: pd.DataFrame, filename: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(filename)
    df.to_parquet(path, compression="gzip")
    print(f"File saved to {path}")
    return path



