#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse
import random

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
mutations_output_dir = main_dir / 'mutations'

if __name__ == "__main__":
    # 1. collect buggy mutation lists
    buggy_mutation_dir = main_dir / 'buggy_mutations'
    buggy_mutation_dict = {}
    total_buggy_mutation = 0
    for file in buggy_mutation_dir.iterdir():
        for mutation in file.iterdir():
            list_file = open(mutation, 'r')
            lines = list_file.readlines()
            for line in lines:
                line = line.strip()
                info = line.split('##')
                mutation_id = info[0]
                mutation_path_origin = info[1]

                if mutation_path_origin not in buggy_mutation_dict:
                    buggy_mutation_dict[mutation_path_origin] = []
                buggy_mutation_dict[mutation_path_origin].append(mutation_id)
                total_buggy_mutation += 1

    print('total buggy mutation: {}'.format(total_buggy_mutation))
    for key in buggy_mutation_dict:
        print('\t{}: {}'.format(key, len(buggy_mutation_dict[key])))

