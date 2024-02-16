#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import sys

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'

def check_dir(dir):
    if not dir.exists():
        dir.mkdir()

if __name__ == "__main__":
    # target_dir = subjects_dir / 'mytest'
    # target_code = target_dir / 'a' / 'b' / 'mytest.c'
    # tc_dir = target_dir / 'TC'
    version = sys.argv[1] # mytest.MUT139.c
    mutation_info = sys.argv[2]
    template_name = sys.argv[3]
    target_dir = subjects_dir / template_name

    # make a directory
    bugs_dir = main_dir / 'bugs'
    check_dir(bugs_dir)

    # make a directory for the new bug
    new_bug = bugs_dir / version
    check_dir(new_bug)

    # make data directory
    data_dir = new_bug / 'data'
    check_dir(data_dir)

    # move template data to new data directory
    template_data = target_dir / 'data'
    cmd = ['cp', '-r', template_data, new_bug]
    sp.call(cmd, cwd=bin_dir)
