# data/psv_loader.py
import pandas as pd

def load_psv(path: str):
    df = pd.read_csv(path, sep="|")
    return df.to_dict(orient="records")
