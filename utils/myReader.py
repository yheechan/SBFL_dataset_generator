import json
import pandas as pd

# input path to json file
# output dict
def get_json_from_file_path(json_file_path) -> dict:
    json_data = {}
    with open(json_file_path, 'r') as fp:
        json_data = json.load(fp)
    return json_data

def get_csv_as_pandas_file_path(file_path):
    df = pd.read_csv(file_path, index_col='lineNo')
    return df
