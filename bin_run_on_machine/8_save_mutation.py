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
    mycore = sys.argv[1]
    mutation_name = sys.argv[2]
    mutation_path_str = sys.argv[3]

    failing_mutations = main_dir / 'buggy_mutations'
    check_dir(failing_mutations)

    file_name = '{}.buggy.mutations.txt'.format(mycore)
    fail_file = failing_mutations / file_name
    if not fail_file.exists():
        fail_file.touch()
    fp = open(fail_file, 'a')
    fp.write('{}##{}\n'.format(mutation_name, mutation_path_str))
