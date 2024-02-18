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

if __name__ == "__main__":
    
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

