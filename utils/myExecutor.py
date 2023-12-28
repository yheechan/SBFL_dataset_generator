import subprocess as sp
from pathlib import Path
import os
from . import myHelper as hh

script_path = Path(os.path.realpath(__file__))
util_dir = script_path.parent
bin_dir = util_dir.parent
main_dir = bin_dir.parent
test_dir = main_dir / 'build/src/test_lib_json'
data_dir = main_dir / 'data'
coverage_dir = main_dir / 'coverage'
spectra_dir = data_dir / 'spectra'
tc_list_file = coverage_dir / 'tc-list.txt'
pretty_dir = coverage_dir / 'pretty'
html_dir = coverage_dir / 'html'
summary_dir = coverage_dir / 'summary'
versions_dir = bin_dir / 'versions'

def remove_all_gcda():
    cmd = [
        'find', '.', '-type',
        'f', '-name', '*.gcda',
        '-delete'
    ]
    res = sp.call(cmd, cwd=main_dir)
    hh.after_exec(res, "removed all *.gcda files.")

def run_by_tc_name(tc_name):
    cmd = [
        './jsoncpp_test',
        '--test',
        tc_name
    ]
    res = sp.call(cmd, cwd=test_dir)
    hh.after_exec(res, "running test case {}\n".format(tc_name))

def run_needed(tc_id, subject):
    if subject == 'summary':
        hh.check_dir(coverage_dir)
        hh.check_dir(summary_dir)
        file_name = tc_id + '.summary.json'
        file_path = summary_dir / file_name
        if file_path.exists():
            return False

    return True

def generate_json_for_TC(tc, file_name):
    hh.check_dir(coverage_dir)
    file_path = coverage_dir / file_name

    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--json', file_path
    ]
    res = sp.call(cmd, cwd=main_dir)
    hh.after_exec(res, "generating json for {} on {}".format(tc, file_name))

    return file_path

def generate_summary_json_for_TC(tc_id):
    hh.check_dir(coverage_dir)
    hh.check_dir(summary_dir)

    file_name = tc_id+'.summary.json'
    file_path = summary_dir / file_name

    if file_path.exists():
        return file_path

    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--json-summary-pretty', '--json', 'json-pretty',
        '-o', file_path
    ]

    res = sp.call(cmd, cwd=main_dir)
    hh.after_exec(res, "generating summary json coverage data using gcovr")

    return file_path

def generate_pretty_json_for_TC(tc_id):
    hh.check_dir(coverage_dir)
    hh.check_dir(pretty_dir)

    file_name = tc_id+'.pretty.json'
    file_path = pretty_dir / file_name

    if file_path.exists():
        return file_path

    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--json', '--json-pretty',
        '-o', file_path
    ]

    res = sp.call(cmd, cwd=main_dir)
    hh.after_exec(res, "generating pretty json coverage data using gcovr")

    return file_path

def generate_html_for_TC(tc_id):
    hh.check_dir(coverage_dir)
    hh.check_dir(html_dir)
    tc_html_dir = html_dir / tc_id
    hh.check_dir(tc_html_dir)

    file_name = 'cov.html'
    file_path = tc_html_dir / file_name

    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--html', '--html-details',
        '-o', file_path,
        '-r', '.'
    ]

    res = sp.call(cmd, cwd=main_dir)
    hh.after_exec(res, "generating html data using gcovr")

    return file_path

def get_test_case_list(tf):
    cmd = [
        './jsoncpp_test',
        '--list-tests'
    ]

    process = sp.Popen(
        cmd, stdout=sp.PIPE, stderr=sp.STDOUT,
        cwd=test_dir, encoding='utf-8'
    )

    raw_tf = []
    raw_tp = []
    while True:
        line = process.stdout.readline()
        if line == '' and process.poll() != None:
            break
        tc_name = line.strip()

        if tc_name in tf:
            raw_tf.append(tc_name)
        else:
            raw_tp.append(tc_name)
    

    raw_tc_list = raw_tf + raw_tp
    tc = {}
    name2id = {}
    tot_cnt = 0
    fail_cnt = 0
    pass_cnt = 0
    num = 1
    for num in range(len(raw_tc_list)):
        tc_id = 'TC'+str(num+1)
        tc_name = raw_tc_list[num]
        type = 'tp'
        if tc_name in tf:
            type = 'tf'
            fail_cnt += 1
        
        assert not tc_id in tc.keys()

        tc[tc_id] = {
            'type': type,
            'name': tc_name
        }
        name2id[tc_name] = tc_id
    
    tot_cnt = len(tc.keys())
    pass_cnt = tot_cnt - fail_cnt
    hh.after_exec(0, "collecting TC lists\n\t> total: {}\n\t> failing: {}\n\t> passing: {}".format(
        tot_cnt, fail_cnt, pass_cnt
    ))

    return [tc, name2id, tot_cnt, fail_cnt, pass_cnt]

