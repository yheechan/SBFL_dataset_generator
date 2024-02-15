#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse
import json
import sys
import csv

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

def add_first_spectra(per_version_dict, cov_json, tc_id, version, line2function_dict):
    for file in cov_json['files']:
        col_data = ['lineNo', tc_id]
        row_data = []

        filename = file['file']
        full_file_name = version+'.'+filename

        if not full_file_name in per_version_dict.keys():
            per_version_dict[full_file_name] = {}
        
        for line in file['lines']:
            cov_result = 1 if line['count'] > 0 else 0

            curr_line_number = line['line_number']
            function_name = return_fuction(filename, curr_line_number, line2function_dict)

            row_name = version+'#'+filename+'#'+function_name+"#"+str(curr_line_number)
            row_data.append([
                row_name, cov_result
            ])
        
        per_version_dict[full_file_name]['col_data'] = col_data
        per_version_dict[full_file_name]['row_data'] = row_data
    return per_version_dict

def add_next_spectra(per_version_dict, cov_json, tc_id, version, line2function_dict):
    for file in cov_json['files']:
        filename = file['file']
        full_file_name = version+'.'+filename
        assert full_file_name in per_version_dict.keys()

        per_version_dict[full_file_name]['col_data'].append(tc_id)

        for i in range(len(file['lines'])):
            line = file['lines'][i]
            curr_line_number = line['line_number']
            function_name = return_fuction(filename, curr_line_number, line2function_dict)

            row_name = version+'#'+filename+'#'+function_name+"#"+str(curr_line_number)
            assert row_name == per_version_dict[full_file_name]['row_data'][i][0]

            cov_result = 1 if line['count'] > 0 else 0

            per_version_dict[full_file_name]['row_data'][i].append(cov_result)
    return per_version_dict

def write_preprocessed_data(project_name, per_version_dict):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    spectra_dir = data_dir / 'spectra'
    check_dir(data_dir)
    check_dir(spectra_dir)

    for file in per_version_dict.keys():
        file_name = file.replace('/', '.') + '.csv'
        row_data = per_version_dict[file]['row_data']
        col_data = per_version_dict[file]['col_data']

        file = spectra_dir / file_name
        with open(file, 'w') as fp:
            cw = csv.writer(fp)
            cw.writerow(col_data)
            cw.writerows(row_data)

if __name__ == "__main__":
    target_dir = subjects_dir / 'mytest'
    target_code = target_dir / 'a' / 'b' / 'mytest.c'
    tc_dir = target_dir / 'TC'
    version = sys.argv[1] # mytest.MUT139.c
    mutation_info = sys.argv[2]

    # 1. get list of test case
    tc_list = get_tc_list(tc_dir)

    # 2. get line to function dict
    line2function_dict = get_line2function_json('mytest', version)

    # # 3. get failing line by reading lines of mutation_info
    # file = sys.argv[3]
    # mutation_fp = open(mutation_info, 'r')
    # mutation_lines = mutation_fp.readlines()
    # for line in mutation_lines:
    #     info = line.strip().split(',')
    #     cmp = info[0]
    #     if version == cmp:
    #         line = int(info[2])
    #         print(info)
    #         break
    #     else:
    #         continue
    
    # # print('failing_file: {}'.format(file))
    # failing_line = line
    # print('failing_line: {}'.format(failing_line))

    per_version_dict = {}
    first = True
    for tc_id in tc_list:
        # get coverage path
        file_name = version + '.' + tc_id + '.raw.json'
        cov_path = target_dir / 'data' / 'coverage' / 'raw' / file_name

        # get coverage as json
        cov_json = get_json(cov_path)

        if first:
            per_version_dict = add_first_spectra(
                per_version_dict,
                cov_json,
                tc_id,
                version,
                line2function_dict
            )
            first = False
        else:
            per_version_dict = add_next_spectra(
                per_version_dict,
                cov_json,
                tc_id,
                version,
                line2function_dict
            )
    
    # write preprocessed_data
    write_preprocessed_data('mytest', per_version_dict)
