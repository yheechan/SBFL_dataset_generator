#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import pandas as pd
import numpy as np
import math

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent

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

    return buggy_line_key

def get_failing_tc(bug_info):
    csv_file_path = bug_info['csv_file_path']
    csv_file_name = bug_info['csv_file_name']
    bug_version_name = bug_info['bug_version_name']
    jsoncpp_src_code = bug_info['jsoncpp_src_code']

    failing_txt_name = bug_version_name + '.txt'
    failing_txt = main_dir / 'overall/failing_testcases' / failing_txt_name
    if not failing_txt.exists():
        print('file not exists: {}'.format(failing_txt))
        exit(1)

    failing_txt_fp = open(failing_txt, 'r')
    failing_list = failing_txt_fp.readlines()
    failing_txt_fp.close()
    failing_list = [x.strip() for x in failing_list]
    
    return failing_list

def get_passing_tc(bug_info, total_cov_dataframe, failing_list):
    passing_list = []
    # go through columns of dataframe
    for tc in total_cov_dataframe.columns[1:]:
        # get the name of the column
        tc_name = tc
        if tc_name not in failing_list:
            passing_list.append(tc_name)
    return passing_list

def get_coincident_tc(buggy_line_key, total_cov_dataframe, passing_list, failing_list):
    coincident_list = []
    # make ac copy of the dataframe
    df = total_cov_dataframe.copy()
    df.set_index('lineNo', inplace=True)

    buggy_line_executing_tc = df.columns[df.loc[buggy_line_key] == 1].tolist()
    # print("Columns with value 1 for row 'b':", columns_with_ones_for_b)
    for tc in buggy_line_executing_tc:
        if tc not in failing_list:
            coincident_list.append(tc)
    return coincident_list

def drop_coincident(total_cov_dataframe, coincident_tc):
    # drop columns with coincident tc
    new_cov_df = total_cov_dataframe.drop(columns=coincident_tc)
    return new_cov_df


def get_spectrum(bug_info, coverage_df, failing_tests):
    X = coverage_df.values.transpose()

    is_failing = np.array([test in failing_tests for test in coverage_df.columns])
    # is_failing = np.array(is_failing).astype(bool)

    # print(bug_info['bug_version_name'])

    # TypeError: ufunc 'invert' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''
    e_p = X[~is_failing].sum(axis=0)
    e_f = X[is_failing].sum(axis=0)
    n_p = np.sum(~is_failing) - e_p
    n_f = np.sum(is_failing) - e_f

    return e_p, e_f, n_p, n_f


def get_spectrum_df(bug_info, coverage_df, failing_tests):
    e_p, e_f, n_p, n_f = get_spectrum(bug_info, coverage_df, failing_tests)
    return e_p, e_f, n_p, n_f

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

def measure_coincidentally_tc():
    spectrum_feature_dir = main_dir / 'overall/spectrum_feature_data_per_bug'
    spec_data_without_coincident_tc_dir = main_dir / 'overall/spectrum_feature_data_excluding_coincidentally_correct_tc_per_bug'
    if not spec_data_without_coincident_tc_dir.exists():
        spec_data_without_coincident_tc_dir.mkdir()
    
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
        buggy_line_key = validate_one_buggy_correct_row(bug_info)
        # print(buggy_line_key)

        postprocessed_cov_dir = main_dir / 'overall/postprocessed_coverage_data'
        cov_csv_list = []
        for cov_csv in postprocessed_cov_dir.iterdir():
            cov_csv_name = cov_csv.name
            if bug_version_name in cov_csv_name:
                cov_csv_list.append(cov_csv)
        
        # concat all cov csv files in cov_csv_list
        total_cov_dataframe = pd.concat([pd.read_csv(x) for x in cov_csv_list], axis=0)
        # assert that buggy line is in the dataframe
        assert buggy_line_key in total_cov_dataframe['lineNo'].values
        # print(total_cov_dataframe.shape)


        # get list of failing test cases
        failing_list = get_failing_tc(bug_info)
        passing_list = get_passing_tc(bug_info, total_cov_dataframe, failing_list)

        # print('{} {} {}'.format(
        #     len(failing_list)+len(passing_list), len(failing_list), len(passing_list)))
        
        coincident_tc = get_coincident_tc(buggy_line_key, total_cov_dataframe, passing_list, failing_list)

        fail_cnt = len(failing_list)
        assert fail_cnt > 0
        pass_cnt = len(passing_list)
        coincident_cnt = len(coincident_tc)
        print(coincident_cnt)
        assert fail_cnt + pass_cnt == 127
        # print('{} {} {}'.format(fail_cnt, pass_cnt, coincident_cnt))

        new_cov_df = drop_coincident(total_cov_dataframe, coincident_tc)
        using_tc_cnt = new_cov_df.shape[1] - 1
        assert using_tc_cnt == (pass_cnt+fail_cnt) - coincident_cnt

        # make 'lineNo' column as index for new_cov_df
        new_cov_df.set_index('lineNo', inplace=True)
        index_nd = new_cov_df.index
        
        e_p, e_f, n_p, n_f = get_spectrum_df(bug_info, new_cov_df, failing_list)
        data = {'ep': e_p, 'ef': e_f, 'np': n_p, 'nf': n_f}

        # calculate SBFL each row at a time
        score_dict = {}
        formula = [
            'Binary', 'GP13', 'Jaccard',
            'Naish1', 'Naish2', 'Ochiai',
            'Russel+Rao', 'Wong1'
        ]
        for form in formula:
            ep_bag = []
            ef_bag = []
            np_bag = []
            nf_bag = []
            score_bag = []
            # measure each group of e_p, e_f, n_p, n_f one by one
            for ep_1, ef_1, np_1, nf_1 in zip(e_p, e_f, n_p, n_f):
                total = ep_1 + ef_1 + np_1 + nf_1
                # print('ep: {} ef: {} np: {} nf: {}'.format(ep_1, ef_1, np_1, nf_1))
                assert total == fail_cnt + (pass_cnt-coincident_cnt)

                score = sbfl(ep_1, ef_1, np_1, nf_1, formula=form)
                # print('form {} score: {}'.format(form, score))
                ep_bag.append(ep_1)
                ef_bag.append(ef_1)
                np_bag.append(np_1)
                nf_bag.append(nf_1)
                score_bag.append(score)
            score_dict[form] = score_bag
        
        for form in score_dict:
            data[form] = score_dict[form]
        
        bug_info = np.zeros_like(e_p)
        data['bug'] = bug_info
        new_df = pd.DataFrame(data, index=index_nd)
        # assert that buggy_line_key is in the index of new_df
        assert buggy_line_key in new_df.index
        # set value 1 to 'bug' column of the row with index 'buggy_line_key'
        new_df.at[buggy_line_key, 'bug'] = 1
        
        new_data_file_name = bug_version_name + '.csv'
        # show the index column to when to csv
        new_df.reset_index(inplace=True)
        new_df.to_csv(spec_data_without_coincident_tc_dir / new_data_file_name, index=False)


if __name__ == "__main__":
    measure_coincidentally_tc()