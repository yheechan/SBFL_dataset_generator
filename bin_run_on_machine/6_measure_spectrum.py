#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse
import json
import sys
import csv
import pandas as pd
import numpy as np

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'

def check_dir(dir):
    if not dir.exists():
        dir.mkdir()

def get_json(json_file_path) -> dict:
    json_data = {}
    with open(json_file_path, 'r') as fp:
        json_data = json.load(fp)
    return json_data

def get_tc_list(tc_dir):
    tc_list = []
    for tc in tc_dir.iterdir():
        tc_name = tc.name
        tc_id = tc_name.split('.')[0]
        tc_list.append(tc_id)
    return tc_list

def get_spectra_list(spectra_dir):
    spectra_list = []
    for file in sorted(spectra_dir.iterdir()):
        spectra_list.append(file)
    return spectra_list

def return_fuction(fname, lnum, line2function_dict):
    endName = fname.split('/')[-1]
    useName = endName if endName == 'CMakeCXXCompilerId.cpp' else fname

    if useName in line2function_dict.keys():
        for funcData in line2function_dict[useName]:
            funcName = funcData[0]
            funcStart = funcData[1]
            funcEnd = funcData[2]

            if lnum >= funcStart and lnum <= funcEnd:
                return funcName
    return 'FUNCTIONNOTFOUND'

def get_line2function_json(project_name, version_num):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    line2function_dir = data_dir / 'line2function'
    check_dir(data_dir)
    check_dir(line2function_dir)

    # version_name = 'bug'+str(version_num)
    version_name = version_num # (mytest.MUT139.c)
    file_name = version_name + '.line2function.json'
    file_path = line2function_dir / file_name

    json_data = {}
    with open(file_path, 'r') as fp:
        json_data = json.load(fp)
    return json_data

def get_spectrum(coverage_df, failing_tests):
    X = coverage_df.values.transpose()

    is_failing = np.array([test in failing_tests for test in coverage_df.columns])

    e_p = X[~is_failing].sum(axis=0)
    e_f = X[is_failing].sum(axis=0)
    n_p = np.sum(~is_failing) - e_p
    n_f = np.sum(is_failing) - e_f

    return e_p, e_f, n_p, n_f

def sbfl(e_p, e_f, n_p, n_f, formula="Ochiai"):
    if formula == "Jaccard":
        divisior = (e_f + n_f + e_p)
        x = np.divide(e_f, divisior, where=divisior!=0)
        return x
    elif formula == "Binary":
        return np.where(n_f > 0, 0, 1)
    elif formula == "GP13":
        divisor = ((2 * e_p) + e_f)
        x = np.divide(e_f, divisor, where=divisor!=0)
        return e_f + x
    elif formula == "Naish1":
        return np.where(n_f > 0, -1, n_p)
    elif formula == "Naish2":
        x = e_p / (e_p + n_p + 1)
        return e_f - x
    elif formula == "Ochiai":
        divisor = np.sqrt((e_f + n_f) * (e_f + e_p))
        return np.divide(e_f, divisor, where=divisor!=0)
    elif formula == "Russel+Rao":
        return e_f/(e_p + n_p + e_f + n_f)
    elif formula == "Wong1":
        return e_f
    else:
        raise Exception(f"Unknown formula: {formula}")

def write_df_to_csv(project_name, df, file_name):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    processed_dir = data_dir / 'processed'
    check_dir(data_dir)
    check_dir(processed_dir)

    csv_file_path = processed_dir / file_name
    df.to_csv(csv_file_path)

    rankLine_dir = data_dir / 'ranked-line'
    check_dir(rankLine_dir)
    csv_file_path = rankLine_dir / file_name
    df.to_csv(csv_file_path)

if __name__ == "__main__":
    target_dir = subjects_dir / 'mytest'
    target_code = target_dir / 'a' / 'b' / 'mytest.c'
    tc_dir = target_dir / 'TC'
    version = sys.argv[1] # mytest.MUT139.c
    mutation_info = sys.argv[2]

    SBFL = [
        'Binary', 'GP13', 'Jaccard', 'Naish1',
        'Naish2', 'Ochiai', 'Russel+Rao', 'Wong1'
    ]

    measured_data = {}
    measured_data['measured'] = {}
    first = True

    # get list of preprocessed data which is per file
    spectra_dir = target_dir / 'data' / 'spectra'
    spectra_list = get_spectra_list(spectra_dir)

    # get failing tc list
    file_nm = version + '.txt'
    failing_file = target_dir / 'data' / 'failing' / file_nm
    failing_fp = open(failing_file, 'r')
    failing_list = failing_fp.readlines()
    failing_list_as_id = []
    for failing in failing_list:
        fail_id = failing.strip().split('/')[-1].split('.')[0]
        failing_list_as_id.append(fail_id)
    
    # get line2function dict
    line2function_dict = get_line2function_json('mytest', version)

    # get failing line by reading lines of mutation_info
    file = sys.argv[3]
    mutation_fp = open(mutation_info, 'r')
    mutation_lines = mutation_fp.readlines()
    for line in mutation_lines:
        info = line.strip().split(',')
        cmp = info[0]
        if version == cmp:
            line = int(info[2])
            print(info)
            break
        else:
            continue
    # print('failing_file: {}'.format(file))
    failing_line = line
    print('failing_line: {}'.format(failing_line))
    # failing file
    failing_file = 'a/b/mytest.c'
    # failing function
    failing_func = return_fuction(failing_file, failing_line, line2function_dict)


    for spectra_csv in spectra_list:
        print(spectra_csv)
        csv_file_name = spectra_csv.name
        bug_version = '.'.join(csv_file_name.split('.')[:3])
        # bug_version = bug_version.split('.')[0] this is original
        # bug_index = int(bug_version[3:])
        print('bug_version: {}'.format(bug_version))

        # get csv as pandas
        spectra_df = pd.read_csv(spectra_csv, index_col='lineNo')
        index_nd = spectra_df.index

        # measure spectra features
        e_p, e_f, n_p, n_f = get_spectrum(spectra_df, failing_list_as_id)
        data = {'ep': e_p, 'ef': e_f, 'np': n_p, 'nf': n_f}

        # calculate SBFL
        for form in SBFL:
            score = sbfl(e_p, e_f, n_p, n_f, formula=form)
            data[form] = score
        
        bug_info = np.zeros_like(e_p)
        data['bug'] = bug_info
        
        bug_key = bug_version + '#' + failing_file + '#' + failing_func + '#' + str(failing_line)

        new_df = pd.DataFrame(data, index=index_nd)
        if bug_key in new_df.index:
            new_df.loc[bug_key, 'bug'] = 1
        write_df_to_csv('mytest', new_df, csv_file_name)
