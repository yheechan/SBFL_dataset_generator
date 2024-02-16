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
# gcovr = main_dir.parent / '.local' / 'bin' / 'gcovr'
gcovr = Path('/home/yangheechan/.local/bin/gcovr')
queue_dir = main_dir / 'afl-test-cases' / 'output' / 'default' / 'queue'

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

def get_test_case_list(project_name, version):
    bug_version = version

    project_path = subjects_dir / project_name
    build_dir = project_path / 'build'

    # get jsoncpp test cases
    cmd = ['./jsoncpp_test', '--list-tests']
    test_dir = build_dir / 'src/test_lib_json'

    if not test_dir.exists():
        print('test directory not found: {}'.format(test_dir))
        exit(1)
    
    process = sp.Popen(
        cmd, stdout=sp.PIPE, stderr=sp.PIPE,
        cwd=test_dir, encoding='utf-8'
    )

    tc_list = []
    name2id = {}
    while True:
        line = process.stdout.readline()
        if line == '' and process.poll() != None:
            break
        tc_name = line.strip()
        tc_list.append(tc_name)
    
    tc = {}
    for num in range(len(tc_list)):
        tc_id = 'TC'+str(num+1)
        tc_name = tc_list[num]

        assert not tc_id in tc.keys()

        tc[tc_id] = {
            'name': tc_name,
            'path': None
        }
        name2id[tc_name] = tc_id
    
    # get afl test cases
    # project_path = subjects_dir / project_name
    # build_dir = project_path / 'build'
    # jsoncpp_fuzzer = build_dir / 'jsoncpp_fuzzer'

    # tc_cnt = len(tc.keys()) - 1
    # for afl_tc in sorted(queue_dir.iterdir()):
    #     tc_cnt += 1
    #     tc_id = 'TC'+str(tc_cnt)
        
    #     afl_name = afl_tc.name
    #     check = afl_name.split(',')[0].split(':')
    #     if check[0] != 'id': continue

    #     afl_num = check[1]
    #     tc_name = 'afl/afl-'+afl_num

    #     assert not tc_id in tc.keys()

    #     # cmd = [jsoncpp_fuzzer, afl_tc]

    #     tc[tc_id] = {
    #         'name': tc_name,
    #         'path': afl_tc
    #     }
    
    return tc, name2id


def remove_all_gcda(project_name):
    project_path = subjects_dir / project_name
    cmd = [
        'find', '.', '-type',
        'f', '-name', '*.gcda',
        '-delete'
    ]
    res = sp.call(cmd, cwd=project_path)

def run_by_tc_name(project_name, tc_name, tc_id, res):
    project_path = subjects_dir / project_name
    build_dir = project_path / 'build'
    test_dir = build_dir / 'src/test_lib_json'
    jsoncpp_test = test_dir / 'jsoncpp_test'

    cmd = [
        jsoncpp_test,
        '--test',
        tc_name
    ]
    sp.call(cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    # hh.after_exec(res, "running {}: {}\n".format(tc_id, tc_name))

if __name__ == "__main__":
    # target_dir = subjects_dir / 'mytest'
    # target_code = target_dir / 'a' / 'b' / 'mytest.c'
    # renew_exe = target_dir / 'renew_cov.sh'

    # tc_dir = target_dir / 'TC'
    version = sys.argv[1]
    mutation_info = sys.argv[2]
    template_name = sys.argv[3]
    get_cov = sys.argv[4]

    # get test cases
    tc, name2id = get_test_case_list(template_name, version)

    fail_exists = 111

    # 1. run test cases
    failing_tc = []
    # for tc in tc_dir.iterdir():
    # MYLIMIT = 10
    # LIMIT_CNT = 0
    for tc_id in tc.keys():
        # tc_name = tc.name
        # tc_id = tc_name.split('.')[0]
        tc_name = tc[tc_id]['name']

        # 0. remove all gcda before running tc
        remove_all_gcda(template_name)

        afl_check = tc_name.split('/')[0]
        # run jsoncpp tc
        if afl_check != 'afl':
            project_path = subjects_dir / template_name
            build_dir = project_path / 'build'
            test_dir = build_dir / 'src/test_lib_json'
            jsoncpp_test = test_dir / 'jsoncpp_test'

            cmd = [
                jsoncpp_test,
                '--test',
                tc_name
            ]
            res = sp.call(cmd, stdout=sp.DEVNULL, stderr=sp.STDOUT)

            # if tc_id in ['TC7', 'TC8', 'TC9', 'TC10', 'TC11', 'TC12']:
            if tc_id in ['TC78', 'TC79', 'TC80']:
                res = 0
            # if LIMIT_CNT == 5:
            #     res = 1
        else:
            project_path = subjects_dir / template_name
            build_dir = project_path / 'build'
            jsoncpp_fuzzer = build_dir / 'jsoncpp_fuzzer'

            tc_path  = tc[tc_id]['path']
            tc_name = 'aflTC-' + tc_path.name.split(',')[0].split(':')[1]

            cmd = [jsoncpp_fuzzer, tc_path]
            res = sp.call(cmd, stdout=sp.DEVNULL, stderr=sp.STDOUT)
        # cmd = [tc]
        # res = sp.call(cmd, stdout=sp.DEVNULL, stderr=sp.STDOUT)
        if res != 0:
            print('{} - [Fail] {} {}:{}'.format(template_name, tc_id, tc_name, res))
            failing_tc.append(tc_id)
            fail_exists = 222
        else:
            print('{} - [Pass] {} {}:{}'.format(template_name, tc_id, tc_name, res))
            
        # 1. generate raw coverage
        if get_cov=='True':
            cov_path = generate_coverage_json(template_name, version, tc_id)
            # cov_json = get_json(cov_path)

        # 2. generate summary
        if get_cov=='True':
            summary_path = generate_summary_json(template_name, version, tc_id)
            # summary_json = get_json(summary_path)

        # 3. renew coverage data
        # cmd = ['bash', renew_exe]
        # res = sp.call(cmd, cwd=target_dir)
        # print('renewing coverage data: {}'.format(res))
        remove_all_gcda(template_name)

        # if LIMIT_CNT == MYLIMIT:
        #     break
        # LIMIT_CNT += 1
    
    # 5. save list of failing test cases to text file
    failing_dir = subjects_dir / template_name / 'data' / 'failing'
    check_dir(failing_dir)
    file_nm = version + '.txt'
    failing_file = failing_dir / file_nm
    if len(failing_tc) != 0:
        with open(failing_file, 'w') as fp:
            for tc in failing_tc:
                fp.write(str(tc) +'\n')
    
    exit(fail_exists)