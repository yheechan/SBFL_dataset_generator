import subprocess as sp
from pathlib import Path
import os
from . import myHelper as hh

script_path = Path(os.path.realpath(__file__))
util_dir = script_path.parent
bin_dir = util_dir.parent
extractor_exe = bin_dir / 'clang-frontend/extractor'
main_dir = bin_dir.parent
build_dir = main_dir / 'build'
preprocessed_dir = main_dir / 'preprocessed'
test_dir = build_dir / 'src/test_lib_json'
data_dir = main_dir / 'data'
coverage_dir = main_dir / 'coverage'
spectra_dir = data_dir / 'spectra'
processed_dir = data_dir / 'processed'
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

def get_ii_files():
    cmd = [
        'find', '.', '-type',
        'f', '-name', '*.ii'
    ]

    process = sp.Popen(
        cmd, stdout=sp.PIPE, stderr=sp.STDOUT,
        cwd=preprocessed_dir, encoding='utf-8'
    )

    ii_files = []
    while True:
        line = process.stdout.readline()
        if line == '' and process.poll() != None:
            break
        line = line.strip()
        if line == '':
            continue
        ii_files.append(line)
    
    return ii_files

def change_ii_to_cpp(ii_files):
    cmd = ['mv']

    cpp_files = []
    if len(ii_files) != 0:
        for file in ii_files:
            cmd.append(file)
            cpp_file_name = file[:-2]+'cpp'
            cmd.append(cpp_file_name)
            cpp_files.append(cpp_file_name)

            res = sp.call(cmd, cwd=preprocessed_dir)
            hh.after_exec(res, "changed {} to {}".format(file, file[:-2]+'cpp'))

            cmd.pop()
            cmd.pop()
    else:
        cmd = [
            'find', '.', '-type',
            'f', '-name', '*.cpp'
        ]

        process = sp.Popen(
            cmd, stdout=sp.PIPE, stderr=sp.STDOUT,
            cwd=preprocessed_dir, encoding='utf-8'
        )

        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() != None:
                break
            line = line.strip()
            if line == '':
                continue
            cpp_files.append(line)
    
    return cpp_files

def extract_line2method(cpp_files):
    cmd = [extractor_exe]

    cnt = 0

    perFile_data = {}
    for file in cpp_files:
        cmd.append(file)

        process = sp.Popen(
            cmd, stdout=sp.PIPE, stderr=sp.STDOUT,
            cwd=preprocessed_dir, encoding='utf-8'
        )

        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() != None:
                break
            line = line.strip()
            if line == '':
                continue

            data = line.split("##")
            # print("class: \t{}".format(data[0]))
            class_name = data[0]
            # print("function: \t{}".format(data[1]))
            function_name = data[1]
            # print("start line: \t{}".format(data[2]))
            start_line = data[2]
            # print("end line: \t{}".format(data[3]))
            end_line = data[3]
            # print("origin file: \t{}".format(data[4]))
            originated_file = data[4]
            file_data = originated_file.split(':')[0]
            route_data = file_data.split('/')
            mark = 0
            for i in range(len(route_data)-1, -1, -1):
                if route_data[i] in ['src', 'build', 'include']:
                    mark = i
                    break
            marked_path = '/'.join(route_data[mark:])
            # print("marked file: {}".format(marked_path))
            # print("targeted file: \t{}".format(data[5]))
            # print("***************\n")

            if not marked_path in perFile_data.keys():
                perFile_data[marked_path] = []
            
            full_function = class_name+'::'+function_name if class_name != 'None' else function_name
            data = (full_function, int(start_line), int(end_line))
            if not data in perFile_data[marked_path]:
                perFile_data[marked_path].append(data)
        
        print('>> extracted line2method from {}'.format(file))
        cmd.pop()
    
    return perFile_data

def get_list_versions():
    version_list = []
    for version in sorted(os.listdir(versions_dir)):
        if version[3].isdigit():
            version_list.append(version) 
    return version_list

def build_version(v_num, onlyProject=False, withPreprocessed=False):
    cmd = [
        './build.py', '--version', str(v_num)
    ]
    if onlyProject:
        cmd.append('--onlyProject')
    if withPreprocessed:
        cmd.append('--withPreprocessed')

    sp.call(cmd, cwd=bin_dir)

def get_list_spectra():
    spectra_list = []
    for spectra in sorted(spectra_dir.iterdir()):
        spectra_list.append(spectra)
    return spectra_list

def get_processed_data_list_on_bug(bug_name):
    processed_data_list = []
    for file in sorted(processed_dir.iterdir()):
        if bug_name in file.name:
            processed_data_list.append(file)
    return processed_data_list