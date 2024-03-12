#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse
import pandas as pd
import numpy as np
import math

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

        if broken_row.shape[0] > 0:
            print('\t{}'.format(file))
            # print the rows of broken row dataframe
            for index, row in broken_row.iterrows():
                # print the value in column with name 'lineNo'
                print('\t\t{}'.format(row['lineNo']))
                print('\t\t{}'.format(row))
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

def validate_one_buggy_line_on_final_data():
    final_dir = main_dir / 'overall/ranked-line'
    count = 0
    for csv_file in final_dir.iterdir():
        out = pd.read_csv(csv_file)
        # check if there is a row that has 'bug' == 1
        # and the number of row with 'bug' == 1 is not 1
        buggy_one = out[out['bug'] == 1]
        if buggy_one.shape[0] != 1:
            print('\t{}'.format(csv_file))
            print('\t\t{}'.format(buggy_one))
        assert buggy_one.shape[0] == 1
        count += 1
    print('1. all {} files have one buggy row'.format(count))
    
def measure_coincidentally_tc():
    final_dir = main_dir / 'overall/spectrum_feature_data_per_bug'
    coincidentally_passing_testcases_per_bug_dir = main_dir / 'overall/coincidentally_passing_testcases_per_bug'
    if not coincidentally_passing_testcases_per_bug_dir.exists():
        coincidentally_passing_testcases_per_bug_dir.mkdir(parents=True, exist_ok=True)
    
    # for csv_file in 
    for csv_file in final_dir.iterdir():
        out = pd.read_csv(csv_file)
        # check that the value of column 'ep', 'ef', 'np', 'nf' add up to exepected_output
        ep = out['ep'].values[0]
        ef = out['ef'].values[0]
        np = out['np'].values[0]
        nf = out['nf'].values[0]
        total = ep + ef + np + nf
        print('{}: {}'.format(csv_file, total))

def copy_mutations_to_directory():
    my_dict = {
        'json_reader': main_dir / 'mutations/src-lib_json-json_reader.cpp-json_reader.cpp/',
        'json_value': main_dir / 'mutations/src-lib_json-json_value.cpp-json_value.cpp/',
    }
    
    final_dir = main_dir / 'overall/spectrum_feature_data_per_bug'
    bug_version_dir = main_dir / 'overall/bug_versions_jsoncpp'
    if not bug_version_dir.exists():
        bug_version_dir.mkdir()
        
    for csv_file in final_dir.iterdir():
        csv_file_name = csv_file.name
        if 'bug' in csv_file_name:
            continue
        mutant_og_id = '.'.join(csv_file_name.split('.')[:3]) # json_reader.MUT132.cpp
        target_file = csv_file_name.split('.')[0] #json_reader
        og = target_file + '.cpp'
        file_dir = bug_version_dir / mutant_og_id
        
        expected_fn = file_dir / og
        
        if not file_dir.exists():
            file_dir.mkdir()
        
        tt_file = my_dict[target_file] / mutant_og_id
        if not tt_file.exists():
            print('non existent: {}'.format(tt_file))
            exit(1)
        
        # copy tt file to file_dir
        sp.run(['cp', '-r', str(tt_file), str(expected_fn)])
        # dir = my_dict[target_file]
        
        
        # if not file_dir.exists():
        #     file_dir.mkdir()

def get_buggy_line_key(buggy_row):
    # get the column 'lineNo' of the row with 'bug' == 1
    buggy_line_key = buggy_row['lineNo'].values[0]
    return buggy_line_key.strip()

def validate_correct_buggy_line(bug_version_name, buggy_line_key):
    bug_version_from_key = buggy_line_key.split('#')[0]
    if bug_version_name != bug_version_from_key:
        print('[invalid] incorrect buggy line: {}'.format(bug_version_name))
        print('\t\tbug version should be {} not {}'.format(bug_version_name, bug_version_from_key))
        # print('\t{}'.format(buggy_line_key))

def validate_one_buggy_correct_row(bug_info):
    csv_file_path = bug_info['csv_file_path']
    csv_file_name = bug_info['csv_file_name']
    bug_version_name = bug_info['bug_version_name']
    jsoncpp_src_code = bug_info['jsoncpp_src_code']

    csv = pd.read_csv(csv_file_path)
    # validate that the number of row with 'bug' == 1 is 1
    buggy_rows = csv[csv['bug'] == 1]                    # retreives dataframe with rows of 'bug' == 1
    if buggy_rows.shape[0] != 1:                         # shape = (row, column)
        print('[invalid] no buggy row: {}'.format(csv_file_path))
        # print('\t{}'.format(buggy_rows))
    
    # get the column 'lineNo' of the row with 'bug' == 1
    buggy_line_key = get_buggy_line_key(buggy_rows)     # json_reader.MUT8538.cpp#src/lib_json/json_reader.cpp#OurReader::readValue()#1144

    # validate that the buggy line is correct
    validate_correct_buggy_line(bug_version_name, buggy_line_key)

def validate_spectrum_data(bug_info):
    csv_file_path = bug_info['csv_file_path']
    csv_file_name = bug_info['csv_file_name']
    bug_version_name = bug_info['bug_version_name']
    jsoncpp_src_code = bug_info['jsoncpp_src_code']

    expected_output = 127
    
    csv = pd.read_csv(csv_file_path)
    # check that the value of column 'ep', 'ef', 'np', 'nf' add up to exepected_output
    ep = csv['ep'].values[0]
    ef = csv['ef'].values[0]
    np = csv['np'].values[0]
    nf = csv['nf'].values[0]
    total = ep + ef + np + nf

    if total != expected_output:
        print('[invalid] total: 127 != {} on {}'.format(total, csv_file_path))


def sbfl(e_p, e_f, n_p, n_f, formula="Ochiai"):
    if formula == "Jaccard":
        denominator = e_f + n_f + e_p
        if denominator == 0:
            return 0
        return e_f / denominator
    elif formula == "Binary":
        if 0 < n_f:
            return 0
        elif n_f == 0:
            return 1
    elif formula == "GP13":
        denominator = 2*e_p + e_f
        if denominator == 0:
            return 0
        return e_f + (e_f / denominator)
    elif formula == "Naish1":
        if 0 < n_f:
            return -1
        elif 0 == n_f:
            return n_p
    elif formula == "Naish2":
        x = e_p / (e_p + n_p + 1)
        return e_f - x
    elif formula == "Ochiai":
        denominator = math.sqrt((e_f + n_f) * (e_f + e_p))
        if denominator == 0:
            return 0
        return e_f / denominator
    elif formula == "Russel+Rao":
        return e_f/(e_p + n_p + e_f + n_f)
    elif formula == "Wong1":
        return e_f
    else:
        raise Exception(f"Unknown formula: {formula}")

def valid_range(score, form):
    if form == 'Binary':
        if score != 0 and score != 1:
            print('invalid score on {}: {}'.format(form, score))
            return False
    elif form == 'GP13':
        if score < 0:
            print('invalid score on {}: {:.4f}'.format(form, score))
            return False
    elif form == 'Jaccard':
        if score < 0 or score > 1:
            print('invalid score on {}: {}'.format(form, score))
            return False
    elif form == 'Naish1':
        if score < -1:
            print('invalid score on {}: {}'.format(form, score))
            return False
    elif form == 'Naish2':
        if score < -1.0: # or # score > #number of failling TC:
            print('invalid score on {}: {}'.format(form, score))
            return False
    elif form == 'Ochiai':
        if score < 0 or score > 1:
            print('invalid score on {}: {}'.format(form, score))
            return False
    elif form == 'Russel+Rao':
        if score < 0 or score > 1:
            print('invalid score on {}: {}'.format(form, score))
            return False
    elif form == 'Wong1':
        if score < 0:
            print('invalid score on {}: {}'.format(form, score))
            return False
    return True
        
def validate_suspicous_score(bug_info):
    formula = [
        'Binary', 'GP13', 'Jaccard',
        'Naish1', 'Naish2', 'Ochiai',
        'Russel+Rao', 'Wong1'
    ]
    csv_file_path = bug_info['csv_file_path']
    csv_file_name = bug_info['csv_file_name']
    bug_version_name = bug_info['bug_version_name']
    jsoncpp_src_code = bug_info['jsoncpp_src_code']

    csv = pd.read_csv(csv_file_path)

    # how to iterate through all the rows in csv

    for index, row in csv.iterrows():
        ep = row['ep']
        ef = row['ef']
        np = row['np']
        nf = row['nf']
        # print(ep, ef, np, nf)
        
        for form in formula:
            past_score = row[form]
            new_score = sbfl(ep, ef, np, nf, formula=form)
            # print(form, calculated_score, score)

            # update csv file to change past score to new score
            # csv.at[index, form] = new_score

            result = valid_range(past_score, form)
            if result == False:
                print('ep {} ef {} np {} nf {}'.format(ep, ef, np, nf))
                print('\t correct score {}'.format(new_score))
                print('\t on following file: {}'.format(csv_file_path))
    
    # csv.to_csv(csv_file_path)

def open_source_code_and_check(
        bug_info, operator,
        og_start_line, og_end_line,
        mut_start_line, mut_end_line,
        og_token, mut_token, total_info
    ):
    csv_file_path = bug_info['csv_file_path']               # path to the csv file
    csv_file_name = bug_info['csv_file_name']               # bug1.csv or json_reader.MUT14.cpp.csv
    bug_version_name = bug_info['bug_version_name']         # bug1 or json_reader.MUT14.cpp
    jsoncpp_src_code = bug_info['jsoncpp_src_code']         # json_value.cpp or json_reader.cpp

    src_code_file = main_dir / 'overall/bug_versions_jsoncpp' / bug_version_name / jsoncpp_src_code
    src_code_fp = open(src_code_file, 'r')
    src_code_lines = src_code_fp.readlines()

    original_src_file = main_dir / 'overall/bug_versions_jsoncpp/original_version' / jsoncpp_src_code
    original_src_fp = open(original_src_file, 'r')
    original_src_lines = original_src_fp.readlines()

    real_og_token = original_src_lines[og_start_line-1].strip()
    bug_mut_token = src_code_lines[mut_start_line-1].strip()
    
    # assert og_token in real_og_token, 'og_token: {} not in {}'.format(og_token, real_og_token)
    a = mut_token not in bug_mut_token
    b = bug_mut_token not in mut_token
    if a and b:
        print('[invalid] Mutation error in source code: {}'.format(bug_version_name))
        print('Source code file: {}'.format(src_code_file))
        # print('\n\ntotal_info: {}'.format(total_info))
        # print('csv_file_path: {}'.format(csv_file_path))
        # print('csv_file_name: {}'.format(csv_file_name))
        # print('bug_version_name: {}'.format(bug_version_name))
        # print('jsoncpp_src_code: {}'.format(jsoncpp_src_code))
        # print('operator: {}'.format(operator))
        
        # print('\nog_src_code_file: {}'.format(original_src_file))
        # print('og_start_line: {}'.format(og_start_line))
        # print('og_end_line: {}'.format(og_end_line))
        # print('og_token: {}'.format(bug_mut_token))

        # print('og_token: {}'.format(og_token))


        # print('\nmut_src_code_file: {}'.format(src_code_file))
        # print('mut_start_line: {}'.format(mut_start_line))
        # print('mut_end_line: {}'.format(mut_end_line))
        # print('mut_token: {}'.format(mut_token))
        

    # assert mut_token in real_mut_token, 'mut_token: {} not in {}'.format(mut_token, real_mut_token)

def validate_mutant_code(bug_info):
    csv_file_path = bug_info['csv_file_path']               # path to the csv file
    csv_file_name = bug_info['csv_file_name']               # bug1.csv or json_reader.MUT14.cpp.csv
    bug_version_name = bug_info['bug_version_name']         # bug1 or json_reader.MUT14.cpp
    jsoncpp_src_code = bug_info['jsoncpp_src_code']         # json_value.cpp or json_reader.cpp

    mut_file_name = jsoncpp_src_code.split('.')[0] + '_mut_db.csv'
    mutant_db = main_dir / 'overall/mutant_db' / mut_file_name
    mutant_fp = open(mutant_db, 'r')
    mutant_lines = mutant_fp.readlines()

    cnt = 0
    for line in mutant_lines:
        if cnt < 2:
            cnt += 1
            continue

        data = line.split(',')
        # print(line)
        mutant_id = data[0]
        operator = data[1]
        og_start_line = int(data[2])
        og_end_line = int(data[4])
        og_token = data[6]
        mut_start_line = int(data[7])
        mut_end_line = int(data[9])
        mut_token = data[11]
        assert og_start_line == mut_start_line
        assert mut_start_line == mut_end_line

        if mutant_id == bug_version_name:
            open_source_code_and_check(
                bug_info, operator,
                og_start_line, og_end_line,
                mut_start_line, mut_end_line,
                og_token, mut_token, line
            )
            break


def validate(dataset, old):
    spectrum_feature_dir = dataset
    print('validating data...')
    for bug_csv in spectrum_feature_dir.iterdir():
        csv_file_name = bug_csv.name
        name_info = csv_file_name.split('.')
        
        bug_version_name = ''
        jsoncpp_src_code = ''
        isfrom_bug = False
        if 'bug' in csv_file_name:
            bug_version_name = name_info[0]
            file_dict = {
                'bug1': 'json_value.cpp',
                'bug2': 'json_reader.cpp',
                'bug3': 'json_reader.cpp',
                'bug4': 'json_reader.cpp',
            }
            jsoncpp_src_code = file_dict[bug_version_name]
            isfrom_bug = True
        else:
            bug_version_name = '.'.join(name_info[:3])  # json_reader.MUT14.cpp
            jsoncpp_src_code = name_info[0] + '.' + name_info[2]
        
        bug_info = {
            'csv_file_path': bug_csv,               # path to the csv file
            'csv_file_name': csv_file_name,         # bug1.csv or json_reader.MUT14.cpp.csv
            'bug_version_name': bug_version_name,   # bug1 or json_reader.MUT14.cpp
            'jsoncpp_src_code': jsoncpp_src_code,   # json_value.cpp or json_reader.cpp
        }

        # 1. validation
        validate_one_buggy_correct_row(bug_info)

        # 2. validate 127
        validate_spectrum_data(bug_info)

        # 3. validate suspcious score
        validate_suspicous_score(bug_info)

        # 4. validate if mutation target token is really within the source code file
        if isfrom_bug != True:
            validate_mutant_code(bug_info)
    
if __name__ == "__main__":
    # spectrum_feature_dir = main_dir / 'overall/spectrum_feature_data_per_bug'
    spec_data_without_coincident_tc_dir = main_dir / 'overall/spectrum_feature_data_excluding_coincidentally_correct_tc_per_bug'

    # validate(spectrum_feature_dir, True)
    validate(spec_data_without_coincident_tc_dir, False)