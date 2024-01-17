import json
import pandas as pd

import subprocess as sp
from pathlib import Path
import os
from . import myHelper as hh

script_path = Path(os.path.realpath(__file__))
util_dir = script_path.parent
tool_dir = util_dir.parent
bin_dir = tool_dir.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'

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

def get_line2function_json(project_name, version_num):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    line2function_dir = data_dir / 'line2function'
    hh.check_dir(data_dir)
    hh.check_dir(line2function_dir)

    version_name = 'bug'+str(version_num)
    file_name = version_name + '.line2function.json'
    file_path = line2function_dir / file_name

    json_data = {}
    with open(file_path, 'r') as fp:
        json_data = json.load(fp)
    return json_data

def get_coincident_tc(project_name, bug_version):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    cov_dir = data_dir / 'coverage'
    coinc_dir = cov_dir / 'coincident'
    hh.check_dir(data_dir)
    hh.check_dir(cov_dir)
    hh.check_dir(coinc_dir)

    file_name = bug_version + '.coincidentTC.txt'
    file_path = coinc_dir / file_name

    coinc_list = []
    with open(file_path, 'r') as fp:
        lines = fp.readlines()

    for line in lines:
        line = line.strip()
        # [tc_id, tc_name]
        data = line.split('#')
        coinc_list.append(data)
    
    return coinc_list