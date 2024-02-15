#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse
import json
import sys

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
subjects_dir = main_dir / 'subjects'
gcovr = main_dir.parent / '.local' / 'bin' / 'gcovr'

def check_dir(dir):
    if not dir.exists():
        dir.mkdir()

def generate_coverage_json(project_name, version, tc_id):
    project_path = subjects_dir / project_name
    data_dir =  project_path / 'data'
    coverage_dir = data_dir / 'coverage'
    raw_dir = coverage_dir / 'raw'
    check_dir(data_dir)
    check_dir(coverage_dir)
    check_dir(raw_dir)

    file_name = version + '.' + tc_id + '.raw.json'
    file_path = raw_dir / file_name
    cmd = [
        gcovr,
        '--gcov-executable', 'llvm-cov gcov',
        '--json', file_path
    ]
    res = sp.call(cmd, cwd=project_path)
    return file_path

def generate_summary_json(project_name, version, tc_id):
    project_path = subjects_dir / project_name
    data_dir =  project_path / 'data'
    coverage_dir = data_dir / 'coverage'
    summary_dir = coverage_dir / 'summary'
    check_dir(data_dir)
    check_dir(coverage_dir)
    check_dir(summary_dir)

    file_name = version + '.' + tc_id + '.summary.json'
    file_path = summary_dir / file_name
    cmd = [
        gcovr,
        '--gcov-executable', 'llvm-cov gcov',
        '--json-summary-pretty', '-o', file_path
    ]
    res = sp.call(cmd, cwd=project_path)
    return file_path

def get_json(json_file_path) -> dict:
    json_data = {}
    with open(json_file_path, 'r') as fp:
        json_data = json.load(fp)
    return json_data

if __name__ == "__main__":
    target_dir = subjects_dir / 'mytest'
    target_code = target_dir / 'a' / 'b' / 'mytest.c'
    renew_exe = target_dir / 'renew_cov.sh'

    tc_dir = target_dir / 'TC'
    version = sys.argv[1]
    mutation_info = sys.argv[2]

    # read lines of mutation_info
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
    
    # print('failing_file: {}'.format(file))
    # print('failing_line: {}'.format(line))
    # failing_line = line

    # failing_file = bugs[bug_version]['file']
    # failing_func = bugs[bug_version]['function']
    # failing_line = bugs[bug_version]['line']

    # row_data = [
    #     ['bug-file-pass'],
    #     ['bug-file-fail'],
    #     ['bug-func-pass'],
    #     ['bug-func-fail'],
    #     ['bug-line-pass'],
    #     ['bug-line-fail']
    # ]
    # col_data = ['criteria']

    # # (pass, fail)
    # execs_buggy_file_cnt = [0, 0]
    # execs_buggy_func_cnt = [0, 0]
    # execs_buggy_line_cnt = [0, 0]
    # # per TC
    # coincident_tc_list = []

    fail_exists = 111

    # 1. run test cases
    failing_tc = []
    for tc in tc_dir.iterdir():
        tc_name = tc.name
        tc_id = tc_name.split('.')[0]
        cmd = [tc]
        res = sp.call(cmd, stdout=sp.DEVNULL, stderr=sp.STDOUT)
        if res != 0:
            print('[Fail] {}:{}'.format(tc_name, res))
            failing_tc.append(tc)
            fail_exists = 222
        else:
            print('[Pass] {}:{}'.format(tc_name, res))

        # 1. generate summary
        cov_path = generate_coverage_json('mytest', version, tc_id)
        # cov_json = get_json(cov_path)

        # 2. generate raw coverage
        summary_path = generate_summary_json('mytest', version, tc_id)

        # 3. renew coverage data
        cmd = ['bash', renew_exe]
        res = sp.call(cmd, cwd=target_dir)
        print('renewing coverage data: {}'.format(res))
    
    # 5. save list of failing test cases to text file
    failing_dir = target_dir / 'data' / 'failing'
    check_dir(failing_dir)
    file_nm = version + '.txt'
    failing_file = failing_dir / file_nm
    with open(failing_file, 'w') as fp:
        for tc in failing_tc:
            fp.write(str(tc) +'\n')
    
    exit(fail_exists)