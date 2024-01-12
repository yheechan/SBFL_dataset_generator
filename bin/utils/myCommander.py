from . import myReader as rr
from . import myWriter as ww
from . import myExecutor as xx
from . import myHelper as hh
import numpy as np
import pandas as pd

def assign_test_cases(db, tf):
    tc_packet = xx.get_test_case_list(tf)
    db.tc = tc_packet[0]
    db.name2id = tc_packet[1]
    db.tc_cnt = tc_packet[2]
    db.tf_cnt = tc_packet[3]
    db.tp_cnt = tc_packet[4]
    return

def return_fuction(fname, lnum, line2method_dict):
    endName = fname.split('/')[-1]
    useName = endName if endName == 'CMakeCXXCompilerId.cpp' else fname

    if useName in line2method_dict.keys():
        for funcData in line2method_dict[useName]:
            funcName = funcData[0]
            funcStart = funcData[1]
            funcEnd = funcData[2]

            if lnum >= funcStart and lnum <= funcEnd:
                return funcName
    return 'FUNCTIONNOTFOUND'

def add_first_spectra(per_version_dict, cov_json, tc_id, version, line2method_dict):
    for file in cov_json['files']:
        col_data = ['lineNo', tc_id]
        row_data = []

        filename = file['file']
        full_file_name = version+'.'+filename

        if not full_file_name in per_version_dict.keys():
            per_version_dict[full_file_name] = {}
        
        for line in file['lines']:
            cov_result = 1 if line['count'] > 0 else 0

            curr_line_number = line['line_number']
            function_name = return_fuction(filename, curr_line_number, line2method_dict)

            row_name = version+'#'+filename+'#'+function_name+"#"+str(curr_line_number)
            row_data.append([
                row_name, cov_result
            ])
        
        per_version_dict[full_file_name]['col_data'] = col_data
        per_version_dict[full_file_name]['row_data'] = row_data
    return per_version_dict

def add_next_spectra(per_version_dict, cov_json, tc_id, version, line2method_dict):
    for file in cov_json['files']:
        filename = file['file']
        full_file_name = version+'.'+filename
        assert full_file_name in per_version_dict.keys()

        per_version_dict[full_file_name]['col_data'].append(tc_id)

        for i in range(len(file['lines'])):
            line = file['lines'][i]
            curr_line_number = line['line_number']
            function_name = return_fuction(filename, curr_line_number, line2method_dict)

            row_name = version+'#'+filename+'#'+function_name+"#"+str(curr_line_number)
            assert row_name == per_version_dict[full_file_name]['row_data'][i][0]

            cov_result = 1 if line['count'] > 0 else 0

            per_version_dict[full_file_name]['row_data'][i].append(cov_result)
    return per_version_dict

def get_spectrum(coverage_df, failing_tests):
    X = coverage_df.values.transpose()

    is_failing = np.array([test in failing_tests for test in coverage_df.columns])

    e_p = X[~is_failing].sum(axis=0)
    e_f = X[is_failing].sum(axis=0)
    n_p = np.sum(~is_failing) - e_p
    n_f = np.sum(is_failing) - e_f

    return e_p, e_f, n_p, n_f

def sbfl(e_p, e_f, n_p, n_f, formula="Ochiai"):
    if formula == "Jaccard":
        return e_f/(e_f + n_f + e_p)
    elif formula == "Binary":
        return np.where(n_f > 0, 0, 1)
    elif formula == "GP13":
        divisor = (2 * e_p + e_f)
        x = np.divide(e_f, divisor, where=divisor!=0)
        return e_f + x
    elif formula == "Naish1":
        return np.where(n_f > 0, -1, n_p)
    elif formula == "Naish2":
        x = e_p / (e_p + n_p + 1)
        return e_f - x
    elif formula == "Ochiai":
        divisor = np.sqrt((e_f + n_f) * (e_f + e_p))
        return np.divide(e_f, divisor, where=divisor!=0)
    elif formula == "Russel+Rao":
        return e_f/(e_p + n_p + e_f + n_f)
    elif formula == "Wong1":
        return e_f
    else:
        raise Exception(f"Unknown formula: {formula}")

def processed_data(db, failing_per_bug, fails):
    SBFL = [
        'Binary', 'GP13', 'Jaccard', 'Naish1',
        'Naish2', 'Ochiai', 'Russel+Rao', 'Wong1'
    ]

    db.processed_data['processed'] = {}
    db.first = True
    spectra_csv_list = xx.get_list_spectra()

    for spectra_csv in spectra_csv_list:
        csv_file_name = spectra_csv.name
        bug_version = csv_file_name.split('.')[0]
        bug_index = int(bug_version[3:])

        print(">> processed data for {}: {}".format(bug_version, csv_file_name))

        failing_list = []
        for failing in failing_per_bug[bug_version]:
            tc_id = db.name2id[failing]
            failing_list.append(tc_id)

        spectra_df = rr.get_csv_as_pandas_file_path(spectra_csv)
        index_nd = spectra_df.index
        e_p, e_f, n_p, n_f = get_spectrum(spectra_df, failing_list)

        data = {'ep': e_p, 'ef': e_f, 'np': n_p, 'nf': n_f}

        for form in SBFL:
            score = sbfl(e_p, e_f, n_p, n_f, formula=form)
            data[form] = score
        
        bug_info = np.zeros_like(e_p)
        data['bug'] = bug_info

        buggy_file = ''
        buggy_line = 0
        buggy_file = fails[bug_version]['file']
        buggy_line = fails[bug_version]['line'][1]
        # for failing in failing_per_bug[bug_version]:
        #     if failing in fails:
        #         buggy_file = fails[failing]['file']
        #         buggy_line = fails[failing]['line'][1]
        
        line2method_dict = rr.get_line2method_json(bug_index)
        function_name = return_fuction(buggy_file, buggy_line, line2method_dict)

        bug_position = bug_version+'#'+buggy_file+'#'+function_name+'#'+str(buggy_line)

        new_df = pd.DataFrame(data, index=index_nd)
        if bug_position in new_df.index:
            new_df.loc[bug_position, 'bug'] = 1
        ww.write_df_to_csv(new_df, csv_file_name)

    output = ">>> [COMPLETE] Generating processed data with generated Spectrum-data."
    print(output)
    return (1, output)

# Define a function to apply to each group
def set_bug_value(group, sbfl_type):
    max_row = group.loc[group[sbfl_type].idxmax()]
    if (group['bug'] == 1).any():
        max_row['bug'] = 1
    return max_row

def ranked_data(db, failing_per_bug, fails):
    SBFL = [
        'Binary', 'GP13', 'Jaccard', 'Naish1',
        'Naish2', 'Ochiai', 'Russel+Rao', 'Wong1'
    ]

    col_data = [''] + SBFL
    row_data = []

    bug_version_list = list(failing_per_bug.keys())
    for bug in bug_version_list:
        if bug not in row_data:
            row_data.append([bug])
        bug_index = row_data.index([bug])

        processed_list = xx.get_processed_data_list_on_bug(bug)
        # save dataframes per fil in list
        dataframe_list = []
        for processed_path in processed_list:
            df = rr.get_csv_as_pandas_file_path(processed_path)
            dataframe_list.append(df)
        
        # concat all dataframes in list
        og_total_df = pd.concat(dataframe_list, axis=0)

        for sbfl_type in SBFL:
            total_df = og_total_df.copy()

            # the index (lineNo) of total_df is a single string formatted as follows:
            # bug_name#file_name#function_name#line_number
            # I want to combine rows that have the same bug_name#file_name#function_name
            # the column values set to the maximum value of a column names sbfl_type
            total_df['key'] = total_df.index.str.extract(r'(bug\d+#.*?#.*?)(?=#|$)', expand=False)
            total_df.columns = total_df.columns.str.strip()

            # set bug value to 1 if any of the rows in the group has a bug value of 1
            result_df = total_df.groupby('key', group_keys=False).apply(set_bug_value, sbfl_type=sbfl_type)
            result_df = result_df.drop(columns='key')

            # sort by column of variable sbfl_type
            result_df = result_df.sort_values(by=sbfl_type, ascending=False)

            file_name = bug+'.'+sbfl_type

            result_df['Rank'] = result_df[sbfl_type].rank(method='max', ascending=False)
            bug_row = result_df[result_df['bug'] == 1]
            bug_rank_value = bug_row['Rank'].values[0]
            row_data[bug_index].append(bug_rank_value)

            ww.write_ranked_data_to_csv(result_df, file_name)

            print(">> ranked data for {}: {} at rank {}".format(bug, file_name, bug_rank_value))
        
    summary_result = {'col_data': col_data, 'row_data': row_data}
    ww.write_ranked_summary_to_csv(summary_result)

    return (1, ">>> [COMPLETE] Generating ranked data with processed data.")



# 1. remove all gcda files
# 2. execute test case
# 3. generate coverage json (line)
# 4. save to DB
# 5. writer spectra data in DB to csv
def spectra_data(db, tf, tp, processed_flag, failing_per_bug, fails):
    tc_names = tf+tp

    version_list = xx.get_list_versions()

    tot_version_dict = []
    for version in version_list:
        version_num = int(version[3:])
        # builds with according version
        # produces ii files for line2method data generation
        # removes the project built for ii
        # build project for coverage
        xx.build_version(version_num, onlyProject=True, withPreprocessed=True)
        line2method_dict = rr.get_line2method_json(version_num)

        per_version_dict = {}
        db.first = True
        for tc_id in db.tc.keys():
            tc_name = db.tc[tc_id]['name']
        # for tc_name in tc_names:
        #     tc_id  = db.name2id[tc_name]

            print(">> spectra data for {}: {}".format(version, tc_id))

            xx.remove_all_gcda()
            check_run = xx.run_needed(version, tc_id, 'raw')
            if check_run[0]:
                xx.run_by_tc_name(tc_name)
                json_file_path = xx.generate_json_for_TC(version, tc_id)
                for_summ = xx.run_needed(version, tc_id, 'summary')
                if for_summ[0]:
                    json_summary_path = xx.generate_summary_json_for_TC_perBUG(version, tc_id)
            else:
                json_file_path = check_run[1]
            cov_json = rr.get_json_from_file_path(json_file_path)

            if db.first:
                per_version_dict = add_first_spectra(
                    per_version_dict,
                    cov_json,
                    tc_id,
                    version,
                    line2method_dict
                )
                db.first = False
            else:
                per_version_dict = add_next_spectra(
                    per_version_dict,
                    cov_json,
                    tc_id,
                    version,
                    line2method_dict
                )
        
        ww.write_spectra_data_to_csv(per_version_dict)
        tot_version_dict.append(per_version_dict)
    
    if processed_flag:
        processed_data(db, failing_per_bug, fails)
    
    output = ">>> [COMPLETE] Generating spectrum-based data with selected Failing & Passing TC."
    print(output)
    return (1, output)# , spectra_file

# 1. executes './jsoncpp_test --list-tests' to gather list of TC
def list_test_cases(db, tf):
    ww.write_test_cases_list_to_txt(db.tc, pp=True)
    output = ">>> [COMPLETE] Generating a text file containing the list of test cases."
    print(output)
    return (1, output)

# 1. remove all gcda files
# 2. execute test case
# 3. generate summary coverage json (file)
def summary_coverage_json_target_TC(db, num):
    tc_id = 'TC'+str(num)

    if not tc_id in db.tc.keys():
        output = ">>> [IN-COMPLETE] summary-json: Test case doesn't exist: {}".format(tc_id)
        print(output)
        return (1, output)

    tc_name = db.tc[tc_id]['name']

    xx.remove_all_gcda()
    xx.run_by_tc_name(tc_name)
    xx.generate_summary_json_for_TC(tc_id)
    
    output = ">>> [COMPLETE] Generating coverage summary in json format {}.".format(tc_id)
    print(output)
    return (1, output)

# 1. remove all gcda files
# 2. execute test case
# 3. generate html
def html_target_TC(db, num):
    tc_id = 'TC'+str(num)

    if not tc_id in db.tc.keys():
        output = ">>> [IN-COMPLETE] html: Test case doesn't exist: {}".format(tc_id)
        print(output)
        return (1, output)

    tc_name = db.tc[tc_id]['name']

    xx.remove_all_gcda()
    xx.run_by_tc_name(tc_name)
    xx.generate_html_for_TC(tc_id)

    output = ">>> [COMPLETE] Generating html of coverage data for {}.".format(tc_id)
    print(output)
    return (1, output)

# 1. remove all gcda files
# 2. execute test case
# 3. generate html
def pretty_json_TC(db, num):
    tc_id = 'TC'+str(num)

    if not tc_id in db.tc.keys():
        output = ">>> [IN-COMPLETE] pretty-json: Test case doesn't exist: {}".format(tc_id)
        print(output)
        return (1, output)

    tc_name = db.tc[tc_id]['name']

    xx.remove_all_gcda()
    xx.run_by_tc_name(tc_name)
    xx.generate_pretty_json_for_TC(tc_id)

    output = ">>> [COMPLETE] Generating coverage in pretty json format for {}.".format(tc_id)
    print(output)
    return (1, output)

def check_exist(target, set):
    found = False
    if target in set:
        found = True
    return found

# Gen one csv containing 0 or 1 for all TC
def criteria_all_TC(db, failing_info):
    failing_file = failing_info['failing_file']
    failing_func = failing_info['failing_func']
    failing_line = failing_info['failing_line']

    row_data = [
        ['bug-file'],
        ['bug-func'],
        ['bug-line'],
    ]
    col_data = ['criteria']

    execs_buggy_file_cnt = 0
    execs_buggy_func_cnt = 0
    execs_buggy_line_cnt = 0
    for tc_id in db.tc.keys():
        col_data.append(tc_id)

        tc_name = db.tc[tc_id]['name']
        xx.remove_all_gcda()
        xx.run_by_tc_name(tc_name)

        # for file criteria
        summ_path = xx.generate_summary_json_for_TC(tc_id)
        summ_json = rr.get_json_from_file_path(summ_path)

        execs_buggy_file = False
        for file in summ_json['files']:
            line_cov = file['line_covered']
            file_name = file['filename']

            if line_cov > 0 and check_exist(file_name, failing_file):
                execs_buggy_file = True
                execs_buggy_file_cnt += 1
                break
            
        row_data[0].append(int(execs_buggy_file))
        print("* {} on fail file".format(execs_buggy_file))


        # for func criteria
        cov_path = xx.generate_pretty_json_for_TC(tc_id)
        cov_json = rr.get_json_from_file_path(cov_path)

        execs_buggy_func = False
        for file in cov_json['files']:
            file_name = file['file']
            for function in file['functions']:
                func_cov = function['execution_count']
                func_name = function['name']

                if func_cov > 0 and check_exist(
                    (file_name, func_name), failing_func
                ):
                    execs_buggy_func = True
                    execs_buggy_func_cnt += 1
                    break
            
            if execs_buggy_func:
                break
        
        row_data[1].append(int(execs_buggy_func))
        print("* {} on fail func".format(execs_buggy_func))

        # for func criteria
        execs_buggy_line = False
        for file in cov_json['files']:
            file_name = file['file']
            for line in file['lines']:
                line_cov = line['count']
                line_no = line['line_number']

                if line_cov > 0 and check_exist(
                    (file_name, line_no), failing_line
                ):
                    execs_buggy_line = True
                    execs_buggy_line_cnt += 1
                    break
            
            if execs_buggy_line:
                break
        
        row_data[2].append(int(execs_buggy_line))
        print("* {} on fail line".format(execs_buggy_line))
    
    db.tc_criteria['col_data'] = col_data
    db.tc_criteria['row_data'] = row_data
    db.tc_criteria['xx_fail_file'] = execs_buggy_file_cnt
    db.tc_criteria['xx_fail_func'] = execs_buggy_func_cnt
    db.tc_criteria['xx_fail_line'] = execs_buggy_line_cnt
    
    ww.write_TC_on_criteria_to_csv(db.tc_criteria)
    ww.write_criteria_stat_results_to_csv(db.tc_criteria, db.tc_cnt)

    output = ">>> [COMPLETE] Generating CSV file for all TC to a criteria."
    print(output)
    return (1, output)

def check(source, dest):
    found = False
    if source == dest:
        found = True
    return found

def criteria_per_BUG(db, bugs, failing_per_bug):

    # per fails
    for bug_name in bugs.keys():
        failing_list = failing_per_bug[bug_name]
        # bug_id = db.name2id[bug_name]
        bug_number = int(bug_name[3:])

        # 1. build version
        xx.build_version(bug_number, onlyProject=True)

        failing_file = bugs[bug_name]['file']
        failing_func = bugs[bug_name]['function']
        failing_line = bugs[bug_name]['line']

        row_data = [
            ['bug-file-pass'],
            ['bug-file-fail'],
            ['bug-func-pass'],
            ['bug-func-fail'],
            ['bug-line-pass'],
            ['bug-line-fail']
        ]
        col_data = ['criteria']

        # (pass, fail)
        execs_buggy_file_cnt = [0, 0]
        execs_buggy_func_cnt = [0, 0]
        execs_buggy_line_cnt = [0, 0]
        # per TC
        for tc_id in db.tc.keys():
            col_data.append(tc_id)

            tc_name = db.tc[tc_id]['name']
            print(bug_name, tc_name)
            # if xx.run_needed(tc_id, 'summary'):
            xx.remove_all_gcda()

            check_run = xx.run_needed(bug_name, tc_id, 'summary')
            if check_run[0]:
                # 2. run TC on current version
                xx.run_by_tc_name(tc_name)
                json_file_path = xx.generate_summary_json_for_TC_perBUG(bug_name, tc_id)
                for_raw = xx.run_needed(bug_name, tc_id, 'raw')
                if for_raw[0]:
                    json_raw_path = xx.generate_json_for_TC(bug_name, tc_id)
            else:
                json_file_path = check_run[1]

            # for file criteria
            summ_json = rr.get_json_from_file_path(json_file_path)

            execs_buggy_file = False
            isFail = False
            # Check through file coverage
            for file in summ_json['files']:
                line_cov = file['line_covered']
                file_name = file['filename']

                # 4. Check if file is covered
                if line_cov > 0 and check(file_name, failing_file):
                    execs_buggy_file = True
                    
                    # 5. Check if file is covered by pass or fail
                    if tc_name in failing_list:
                        execs_buggy_file_cnt[1] += 1
                        isFail = True
                    else:
                        execs_buggy_file_cnt[0] += 1
                        isFail = False
                    break
            
            # 6. if file is covered, save on whether it is fail or pass
            if execs_buggy_file:
                row_data[0].append(int(not isFail))
                row_data[1].append(int(isFail))
            else:
                row_data[0].append(0)
                row_data[1].append(0)
            print("* {} on fail file".format(execs_buggy_file))

            # for func criteria
            check_run = xx.run_needed(bug_name, tc_id, 'raw')
            if check_run[0]:
                xx.run_by_tc_name(tc_name)
                json_file_path = xx.generate_json_for_TC(bug_name, tc_id)
            else:
                json_file_path = check_run[1]
            # cov_path = xx.generate_pretty_json_for_TC(tc_id)
            cov_json = rr.get_json_from_file_path(json_file_path)

            execs_buggy_func = False
            isFail = False
            # check through function of each file coverage
            for file in cov_json['files']:
                file_name = file['file']
                for function in file['functions']:
                    func_cov = function['execution_count']
                    func_name = function['name']

                    # 7. Check if function is covered
                    if func_cov > 0 and check((file_name, func_name), failing_func):
                        execs_buggy_func = True

                        # 8. Check if function is covered by pass or fail
                        if tc_name in failing_list:
                            execs_buggy_func_cnt[1] += 1
                            isFail = True
                        else:
                            execs_buggy_func_cnt[0] += 1
                            isFail = False
                        break
                
                if execs_buggy_func:
                    break
            
            # 9. if function is covered, save on whether it is fail or pass
            if execs_buggy_file:
                row_data[2].append(int(not isFail))
                row_data[3].append(int(isFail))
            else:   
                row_data[2].append(0)
                row_data[3].append(0)
            print("* {} on fail func".format(execs_buggy_func))

            # for func criteria
            execs_buggy_line = False
            isFail = False
            # 10. check through line of each file coverage
            for file in cov_json['files']:
                file_name = file['file']
                for line in file['lines']:
                    line_cov = line['count']
                    line_no = line['line_number']

                    # 11. Check if line is covered
                    if line_cov > 0 and check((file_name, line_no), failing_line):
                        execs_buggy_line = True

                        # 12. Check if line is covered by pass or fail
                        if tc_name in failing_list:
                            execs_buggy_line_cnt[1] += 1
                            isFail = True
                        else:
                            execs_buggy_line_cnt[0] += 1
                            isFail = False
                        break
                
                if execs_buggy_line:
                    break
            
            # 13. if line is covered, save on whether it is fail or pass
            if execs_buggy_line:
                row_data[4].append(int(not isFail))
                row_data[5].append(int(isFail))
            else:
                row_data[4].append(0)
                row_data[5].append(0)
            print("* {} on fail line".format(execs_buggy_line))

        db.tc_criteria['target'] = bug_name
        db.tc_criteria['col_data'] = col_data
        db.tc_criteria['row_data'] = row_data
        db.tc_criteria['xx_fail_file'] = execs_buggy_file_cnt
        db.tc_criteria['xx_fail_func'] = execs_buggy_func_cnt
        db.tc_criteria['xx_fail_line'] = execs_buggy_line_cnt

        ww.write_TC_on_criteria_per_BUG_to_csv(db.tc_criteria)
        ww.write_criteria_stat_results_per_BUG_to_csv(db.tc_criteria, db.tc_cnt)

    output = ">>> [COMPLETE} Generating CSV file for all TC to a criteria per BUG."
    print(output)
    return (1, output)

def save_total_cov_info_on_DB(db):

    for tc_id in db.tc.keys():
        # initiate tc_id to relation dict
        assert not tc_id in db.tc_relation.keys()
        db.all_cov[tc_id] = {
            'files': [],
            'functions': [],
            'lines': []
        }

        tc_name = db.tc[tc_id]['name']
        xx.remove_all_gcda()
        xx.run_by_tc_name(tc_name)

        # for file relation
        summ_path = xx.generate_summary_json_for_TC(tc_id)
        summ_json = rr.get_json_from_file_path(summ_path)

        for file in summ_json['files']:
            line_cov = file['line_covered']
            file_name = file['filename']

            if line_cov > 0:
                db.all_cov[tc_id]['files'].append(file_name)
        
        # for func relation
        cov_path = xx.generate_pretty_json_for_TC(tc_id)
        cov_json = rr.get_json_from_file_path(cov_path)

        for file in cov_json['files']:
            file_name = file['file']
            for function in file['functions']:
                func_cov = function['execution_count']
                func_name = function['name']

                if func_cov > 0:
                    db.all_cov[tc_id]['functions'].append(
                        (file_name, func_name)
                    )
            
            for line in file['lines']:
                line_cov = line['count']
                line_no = line['line_number']

                if line_cov > 0:
                    db.all_cov[tc_id]['lines'].append(
                        (file_name, line_no)
                    )
    return 0

def relation_all_TC(db):
    res = save_total_cov_info_on_DB(db)
    hh.after_exec(res, "gathered all info on covrage for all TC")

    db.tc_relation['file-intersection'] = {
        'col_data': ['# of intersecting files'],
        'row_data': []
    }
    db.tc_relation['func-intersection'] = {
        'col_data': ['# of intersecting functions'],
        'row_data': []
    }
    db.tc_relation['line-intersection'] = {
        'col_data': ['# of intersecting lines'],
        'row_data': []
    }

    # initialize csv data
    for tc_id in db.tc.keys():
        db.tc_relation['file-intersection']['col_data'].append(tc_id)
        db.tc_relation['func-intersection']['col_data'].append(tc_id)
        db.tc_relation['line-intersection']['col_data'].append(tc_id)

        db.tc_relation['file-intersection']['row_data'].append([tc_id])
        db.tc_relation['func-intersection']['row_data'].append([tc_id])
        db.tc_relation['line-intersection']['row_data'].append([tc_id])

    tc_id = list(db.all_cov.keys())
    for row in range(len(db.all_cov)):
        # compare row to each col
        x_file_set = set(db.all_cov[tc_id[row]]['files'])
        x_func_set = set(db.all_cov[tc_id[row]]['functions'])
        x_line_set = set(db.all_cov[tc_id[row]]['lines'])

        for col in range(0, row):
            y_file_list = db.all_cov[tc_id[col]]['files']
            y_func_list = db.all_cov[tc_id[col]]['functions']
            y_line_list = db.all_cov[tc_id[col]]['lines']

            file_cnt = len(list(x_file_set.intersection(y_file_list)))
            func_cnt = len(list(x_func_set.intersection(y_func_list)))
            line_cnt = len(list(x_line_set.intersection(y_line_list)))

            db.tc_relation['file-intersection']['row_data'][row].append(file_cnt)
            db.tc_relation['func-intersection']['row_data'][row].append(func_cnt)
            db.tc_relation['line-intersection']['row_data'][row].append(line_cnt)
    
    ww.write_data_to_csv(db.tc_relation['file-intersection'], 'file_intersection')
    ww.write_data_to_csv(db.tc_relation['func-intersection'], 'func_intersection')
    ww.write_data_to_csv(db.tc_relation['line-intersection'], 'line_intersection')

    output = ">>> [COMPLETE] Generating TC-to-TC relation csv on per-file, per-function, per-line intersections."
    print(output)
    return (1, output)
