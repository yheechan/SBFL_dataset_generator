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

def validate_broken_row():
    rankedLines = main_dir / 'overall' / 'ranked-line'

    print('validating broken row for ranked line')
    for file in rankedLines.iterdir():
        file_name = file.name
        file_version = file_name.split('.')[0]
        file_type = file_name.split('.')[1]

        if file_type == 'rank':
            continue

        fp = open(file, 'r')
        lines = fp.readlines()
        out = pd.read_csv(file)
        
        # assert all value in all columns of all rows are not null
        assert out.isnull().values.any() == False
    print('\tno broken lines')

if __name__ == "__main__":
    validate_broken_row()