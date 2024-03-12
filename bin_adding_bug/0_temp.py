#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse
import pandas as pd

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
mutations_output_dir = main_dir / 'mutations'
bugs_dir = main_dir / 'bugs'

def check_duplicate_tc():
    selected_files = [
        main_dir / 'selected_mutation.txt',
        main_dir / 'selected_mutation-v1.txt'
    ]

    all_list = []
    file_dict = {}

    for file in selected_files:
        fp = open(file, 'r')
        lines = fp.readlines()
        for line in lines:
            line = line.strip()
            info = line.split(',')
            mutation_id = info[0]

            line = info[1]
            fileType = mutation_id.split('.')[0]
            if fileType not in file_dict:
                file_dict[fileType] = []
            
            if line in file_dict[fileType]:
                print('duplicated in line: {}'.format(line))
            file_dict[fileType].append(line)

            if mutation_id in all_list:
                print('duplicated mutant: {}'.format(mutation_id))
            all_list.append(mutation_id)

# Custom sorting function
def custom_sort(line):
    parts = line.split(' | ')
    return (parts[0].split('.')[0], int(parts[0].split('.')[1][3:]))

def make_mutation_table():
    rankedLines = main_dir / 'overall/spectrum_feature_data_per_bug'

    mutation_db = {
        'json_reader': main_dir / 'mutations/src-lib_json-json_reader.cpp-json_reader.cpp/json_reader_mut_db.csv',
        'json_value': main_dir / 'mutations/src-lib_json-json_value.cpp-json_value.cpp/json_value_mut_db.csv',
    } 
        

    mutant_line_info = []
    for file in rankedLines.iterdir():
        filename = file.name
        target_src_file = filename.split('.')[0]
        mutant_id = '.'.join(filename.split('.')[:3])

        if 'bug' in target_src_file:
            # print(target_src_file)
            continue

        target_db = mutation_db[target_src_file]
        target_fp = open(target_db, 'r')
        target_lines = target_fp.readlines()

        found = False
        for line in target_lines:
            info = line.split(',')
            if info[3] == 'Before Mutation':
                continue
            
            db_mutant_id = info[0]
            json_file = target_src_file + '.cpp'
            line_no = info[2]
            operator = info[1]
            before_mutation = info[6]
            after_mutation = info[11]
            if db_mutant_id == mutant_id:
                data = '{} | {} | {} | {} | {} | {}'.format(
                    db_mutant_id, json_file, line_no,
                    operator, before_mutation, after_mutation
                )
                mutant_line_info.append(data)
                found = True
        if found == False:
            print('not found: {}'.format(mutant_id))
    
    sorted_mutant_lines = sorted(mutant_line_info, key=custom_sort)
    cnt = 5
    for line in sorted_mutant_lines:
        print('{} | {}'.format(cnt, line))
        cnt += 1


if __name__ == "__main__":
    # check_duplicate_tc()
    make_mutation_table()