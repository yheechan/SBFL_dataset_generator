#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse
import pandas as pd

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
# mutations_output_dir = main_dir / 'mutations'
bugs_dir = main_dir / 'bugs'

def check_dir(dir):
    if not dir.exists():
        dir.mkdir()

def copy_data(src_dir, dest_dir, bug_versions):
    check_dir(dest_dir)

    # summary_files = []

    included_cnt = 0
    for bug in bug_versions:
        
        # ok to copy
        data_dir = bug / 'data' / src_dir
        bug_name = bug.name
        for filepath in data_dir.iterdir():
            # check if bug_name is a substring of the file name string
            if bug_name not in filepath.name:
                continue
            sp.call(['cp', str(filepath), str(dest_dir)])

            included_cnt += 1

    print(f'included_cnt {included_cnt} files')
    

if __name__ == "__main__":
    
    selected_versions = []
    excluded_versions = []
    no_buggy_line_mutants = []
    fail_without_buggy_line_execution = []
    # pass_with_buggy_line_execution = []
    list_fail_tc_not_executing_buggy_line_per_target = {}
    for machines in sorted(bugs_dir.iterdir()):
        machines = machines / 'bugs'
        for target in sorted(machines.iterdir()):
            exclude_status = False

            target_id = target.name
            if target_id == 'bugs': continue

            csv_name = target_id + '.csv'
            rankedLines = target / 'data/ranked-line' / csv_name
            out = pd.read_csv(rankedLines)

            # [1] check if buggy line exists in ranked-line data
            no_buggy_line_status = False
            buggy_one = out[out['bug'] == 1]
            # buggy line not exists in datset
            if buggy_one.shape[0] != 1:
                exclude_status = True
                no_buggy_line_status = True
                no_buggy_line_mutants.append(target_id)
            
            # [2] check for mutant line not executed but still fail
            # buggy row ('bug' == 1)...
            # execute and fail ('ef' == 0)
            does_exists = out[(out['bug'] == 1) & (out['ef'] == 0)].shape[0] > 0
            # mutant line (buggy line) is not executed but fails exists
            if does_exists:
                exclude_status = True
                fail_without_buggy_line_execution.append(target_id)
            
            # # [3] check for mutant line is executed and passes
            # # buggy row ('bug' == 1)...
            # # execute and pass ('ep' == 1)
            # does_exists = out[(out['bug'] == 1) & (out['ep'] == 1)].shape[0] > 0
            # # mutant line (buggy line) is executed and passes
            # if does_exists:
            #     exclude_status = True
            #     pass_with_buggy_line_execution.append(target_id)
            
            # [4] check where failing test cases does not execute buggy line
            # retreiving list of failing tc
            if no_buggy_line_status==False:
                txt_name = target_id + '.txt'
                failing_tc_list_file = target / 'data/failing' / txt_name
                failing_fp = open(failing_tc_list_file, 'r')
                failing_list = failing_fp.readlines()

                # retreiving value of column named 'lineNo' where column 'bug' == 1
                buggy_line_key = out[out['bug'] == 1]['lineNo'].values[0].strip()
                key_info = buggy_line_key.split('#')

                # get the buggy spectra data
                mutant_version_id = key_info[0]
                file_path = key_info[1].replace('/', '.')
                buggy_spectra_csv_name = mutant_version_id + '.' + file_path + '.csv'
                buggy_spectra_csv_path = target / 'data/spectra' / buggy_spectra_csv_name
                spectra_data = pd.read_csv(buggy_spectra_csv_path)

                # check if failing tc executes buggy line
                # yes = 0
                # tott = 0
                # no = 0
                for failing in failing_list:
                    # tott+=1
                    tc_id = failing.strip()

                    # where column 'lineNo' == buggy_line_key
                    # and column tc_id == 0
                    # if exists then add to list_fail_tc_not_executing_buggy_line_per_target
                    # lineNo is a string value
                    does_exists = spectra_data[(spectra_data['lineNo'] == buggy_line_key) & (spectra_data[tc_id] == 0)].shape[0] > 0
                    # yessy = spectra_data[(spectra_data['lineNo'] == buggy_line_key) & (spectra_data[tc_id] == 1)].shape[0] > 0
                    # if yessy: yes+=1
                    if does_exists:
                        # no+=1
                        if target_id not in list_fail_tc_not_executing_buggy_line_per_target:
                            list_fail_tc_not_executing_buggy_line_per_target[target_id] = []
                        list_fail_tc_not_executing_buggy_line_per_target[target_id].append(tc_id)
                # if yes > 0:
                #     print('{}/{}\t{}/{}'.format(yes, tott, no, tott))
            # failing tc not executing buggy line exists
            if target_id in list_fail_tc_not_executing_buggy_line_per_target:
                exclude_status = True

            if exclude_status:
                excluded_versions.append(target)
            else:
                selected_versions.append(target)


    print('no_buggy_line_mutants: {}'.format(len(no_buggy_line_mutants)))
    # no_bug_line_txt = main_dir / 'invalid_no_bug_line.txt'
    # no_bug_line_fp = open(no_bug_line_txt, 'w')
    # for no_bug in no_buggy_line_mutants:
    #     no_bug_line_fp.write(no_bug+'\n')
    

    print('fail_without_buggy_line_execution: {}'.format(len(fail_without_buggy_line_execution)))
    # print('pass_with_buggy_line_execution: {}'.format(len(pass_with_buggy_line_execution)))
    print('list_fail_tc_not_executing_buggy_line_per_target: {}'.format(len(list_fail_tc_not_executing_buggy_line_per_target)))

    print('total bugs: {}'.format(len(selected_versions)))

    perfile_cnt = {}
    for bug in selected_versions:
        file_name = bug.name
        indic = file_name.split('.')[0]
        if indic not in perfile_cnt:
            perfile_cnt[indic] = 0
        perfile_cnt[indic] += 1
    for key in perfile_cnt:
        print('{}: {}'.format(key, perfile_cnt[key]))

    
    overall_dir = main_dir / 'overall'
    check_dir(overall_dir)
    
    # make coverage directory
    coverage_dir = overall_dir / 'coverage'
    check_dir(coverage_dir)
    
    # copy coverage data
    copy_data('coverage/raw', coverage_dir / 'raw', selected_versions)

    # copy summary data
    copy_data('coverage/summary', coverage_dir / 'summary', selected_versions)

    # copy spectra data
    copy_data('spectra', overall_dir / 'spectra', selected_versions)

    # copy processed data
    copy_data('processed', overall_dir / 'processed', selected_versions)

    # copy ranked-line
    copy_data('ranked-line', overall_dir / 'ranked-line', selected_versions)

    # copy failing
    copy_data('failing', overall_dir / 'failing', selected_versions)

    # line2function
    copy_data('line2function', overall_dir / 'line2function', selected_versions)

