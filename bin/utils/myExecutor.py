import subprocess as sp
from pathlib import Path
import os
from . import myHelper as hh

script_path = Path(os.path.realpath(__file__))
util_dir = script_path.parent
bin_dir = util_dir.parent
main_dir = bin_dir.parent
src_dir = main_dir / 'src'
extractor_exe = bin_dir / 'extractor'
subjects_dir = main_dir / 'subjects'

versions_dir = src_dir / 'bug-versions-jsoncpp'

def remove_all_gcda(project_name):
    project_path = subjects_dir / project_name
    cmd = [
        'find', '.', '-type',
        'f', '-name', '*.gcda',
        '-delete'
    ]
    res = sp.call(cmd, cwd=project_path)
    hh.after_exec(res, "removed all *.gcda files.")

def run_by_tc_name(project_name, tc_name):
    project_path = subjects_dir / project_name
    build_dir = project_path / 'build'
    test_dir = build_dir / 'src/test_lib_json'

    cmd = [
        './jsoncpp_test',
        '--test',
        tc_name
    ]
    res = sp.call(cmd, cwd=test_dir)
    hh.after_exec(res, "running test case {}\n".format(tc_name))

def run_needed(project_name, version, tc_id, type):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    coverage_dir = data_dir / 'coverage'
    hh.check_dir(data_dir)
    hh.check_dir(coverage_dir)

    file_name = version + '.' + tc_id + '.' + type + '.json'

    raw_dir = coverage_dir / 'raw'
    summary_dir = coverage_dir / 'summary'

    start_path = raw_dir
    if type == 'raw':
        hh.check_dir(raw_dir)
        start_path = raw_dir
    elif type == 'pretty':
        hh.check_dir(summary_dir)
        start_path = summary_dir

    file_path = start_path / file_name

    if file_path.exists():
        return (False, file_path)

    return (True, 0)

def generate_json_for_TC(project_name, version, tc_id):
    project_path = subjects_dir / project_name
    data_dir =  project_path / 'data'
    coverage_dir = data_dir / 'coverage'
    raw_dir = coverage_dir / 'raw'
    hh.check_dir(data_dir)
    hh.check_dir(coverage_dir)
    hh.check_dir(raw_dir)

    file_name = version + '.' + tc_id + '.raw.json'
    file_path = raw_dir / file_name
    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--json', file_path
    ]
    res = sp.call(cmd, cwd=project_path)
    hh.after_exec(res, "generating json for {} on {}".format(tc_id, file_name))
    return file_path

def generate_summary_json_for_TC(project_name, tc_id):
    project_path = subjects_dir / project_name
    data_dir =  project_path / 'data'
    coverage_dir = data_dir / 'coverage'
    summary_dir = coverage_dir / 'summary'
    hh.check_dir(data_dir)
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

    res = sp.call(cmd, cwd=project_path)
    hh.after_exec(res, "generating summary json coverage data using gcovr")

    return file_path

def generate_summary_json_for_TC_perBUG(project_name, bug_name, tc_id):
    project_path = subjects_dir / project_name
    data_dir =  project_path / 'data'
    coverage_dir = data_dir / 'coverage'
    summary_dir = coverage_dir / 'summary'
    hh.check_dir(data_dir)
    hh.check_dir(coverage_dir)
    hh.check_dir(summary_dir)

    file_name = bug_name+ '.' + tc_id+'.summary.json'
    file_path = summary_dir / file_name

    if file_path.exists():
        return file_path

    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--json-summary-pretty', '--json', 'json-pretty',
        '-o', file_path
    ]

    res = sp.call(cmd, cwd=project_path)
    hh.after_exec(res, "generating summary json coverage data using gcovr")

    return file_path

def generate_pretty_json_for_TC(project_name, tc_id):
    project_path = subjects_dir / project_name
    data_dir =  project_path / 'data'
    coverage_dir = data_dir / 'coverage'
    pretty_dir = coverage_dir / 'pretty'
    hh.check_dir(data_dir)
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

    res = sp.call(cmd, cwd=project_path)
    hh.after_exec(res, "generating pretty json coverage data using gcovr")

    return file_path

def generate_html_for_TC(project_name, tc_id):
    project_path = subjects_dir / project_name
    data_dir =  project_path / 'data'
    coverage_dir = data_dir / 'coverage'
    html_dir = coverage_dir / 'html'
    hh.check_dir(data_dir)
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

def get_test_case_list(project_name, tf):
    project = project_name.split('-')[0]
    bug_version = project_name.split('-')[1]

    project_path = subjects_dir / project_name
    build_dir = project_path / 'build'
    if not project_path.exists() or not build_dir.exists():
        cmd = [
            './build.py', '--project', project, '--bug_version', bug_version,
            '--onlyProject', '--withPreprocessed'
        ]
        sp.call(cmd, cwd=bin_dir)

    cmd = [
        './jsoncpp_test',
        '--list-tests'
    ]

    test_dir = build_dir / 'src/test_lib_json'

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

def get_ii_files(project_path):
    cmd = [
        'find', '.', '-type',
        'f', '-name', '*.ii'
    ]

    preprocessed_dir = project_path / 'preprocessed'

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

def change_ii_to_cpp(project_path, ii_files):
    preprocessed_dir = project_path / 'preprocessed'

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

def extract_line2method(project_path, cpp_files):
    preprocessed_dir = project_path / 'preprocessed'

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

def build_version(project_name, onlyProject=False, withPreprocessed=False):
    project = project_name.split('-')[0]
    bug_version = project_name.split('-')[1]
    cmd = [
        './build.py', '--project', project, '--bug_version', bug_version, '--withPreprocessed'
    ]
    
    project_path = subjects_dir / project_name
    build_dir = project_path / 'build'
    if build_dir.exists():
        return

    sp.call(cmd, cwd=bin_dir)

def get_list_spectra(project_name):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    spectra_dir = data_dir / 'spectra'
    spectra_list = []
    for spectra in sorted(spectra_dir.iterdir()):
        spectra_list.append(spectra)
    return spectra_list

def get_processed_data_list_on_bug(project_name, bug_name):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    processed_dir = data_dir / 'processed'
    processed_data_list = []
    for file in sorted(processed_dir.iterdir()):
        if bug_name in file.name:
            processed_data_list.append(file)
    return processed_data_list