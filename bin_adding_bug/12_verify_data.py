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
        out = pd.read_csv(file)
        # check whether there is a broken row
        broken_row = out[out.isnull().any(axis=1)]
        assert broken_row.shape[0] == 0
            

    print('\tno broken lines')

def validate_buggy_row():
    # check the number of row with column 'bug' == 1
    print('validating invalidity (does not contain buggy row')
    rankedLines = main_dir / 'overall' / 'ranked-line'
    invalid_buggy_row_cnt = 0
    for file in rankedLines.iterdir():
        file_name = file.name
        mutant_id = '.'.join(file_name.split('.')[:3])
        
        out = pd.read_csv(file)
        buggy_one = out[out['bug'] == 1]
        
        if buggy_one.shape[0] != 1:
            invalid_buggy_row_cnt += 1
            # print('\t{}'.format(mutant_id))
    print('\ttotal # of mutant data that are invalid: {}'.format(invalid_buggy_row_cnt))

def mutant_line_not_executed_but_still_fail():
    tg = main_dir / 'overall' / 'ranked-line'

    print('validating invalidity (mutant line not executed but still fail)')
    total_cnt = 0
    diff_cnt = {}
    for file in tg.iterdir():
        out = pd.read_csv(file)

        # check if a row that
        # has 'bug' column == 1
        # bug 'ef' column == 0
        does_exists = out[(out['bug'] == 1) & (out['ef'] == 0)].shape[0] > 0

        file_name = file.name
        mutant_id = '.'.join(file_name.split('.')[:3])

        key = file_name.split('.')[0]
        if key not in diff_cnt:
            diff_cnt[key] = 0

        if does_exists:
            diff_cnt[key] += 1
            print('\t{}: {}'.format(mutant_id, does_exists))
            total_cnt += 1
    print('\t{} files'.format(total_cnt))
    for file_name in diff_cnt:
        print('\t\t{}: {}'.format(file_name, diff_cnt[file_name]))

if __name__ == "__main__":
    validate_broken_row()
    validate_buggy_row()
    mutant_line_not_executed_but_still_fail()