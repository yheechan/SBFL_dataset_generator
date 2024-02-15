#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'

if __name__ == "__main__":
    target_dir = subjects_dir / 'mytest'
    target_code = target_dir / 'a' / 'b' / 'mytest.c'

    # clean
    clean = 'clean.sh'
    cmd = ['bash', clean]
    res = sp.call(cmd, cwd=target_dir)
    if res != 0:
        print('clean failed: {}'.format(res))
        exit(1)

    # get preprocessed code
    cmd = ['clang', '-E', target_code, '-o', target_dir / 'pp.c']
    res = sp.call(cmd, cwd=bin_dir, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    if res != 0:
        print('preprocessing code failed: {}'.format(res))
        exit(1)

    # compile code
    cmd = [
        'clang', '-O0',
        '-fprofile-arcs', '-ftest-coverage', '-g',
        target_code, '-o', target_dir / 'a' / 'b' / 'mytest'
    ]
    res = sp.call(cmd, cwd=target_dir / 'a' / 'b', stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    if res != 0:
        print('compiling code failed: {}'.format(res))
        exit(1)