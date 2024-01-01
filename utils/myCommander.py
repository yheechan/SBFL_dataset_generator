from . import myReader as rr
from . import myWriter as ww
from . import myExecutor as xx
from . import myHelper as hh

def assign_test_cases(db, tf):
    tc_packet = xx.get_test_case_list(tf)
    db.tc = tc_packet[0]
    db.name2id = tc_packet[1]
    db.tc_cnt = tc_packet[2]
    db.tf_cnt = tc_packet[3]
    db.tp_cnt = tc_packet[4]
    return

def add_first_spectra(per_version_dict, cov_json, tc_id, version):
    for file in cov_json['files']:
        col_data = ['lineNo', tc_id]
        row_data = []

        full_file_name = version+'.'+file['file']

        if not full_file_name in per_version_dict.keys():
            per_version_dict[full_file_name] = {}
        
        for line in file['lines']:
            cov_result = 1 if line['count'] > 0 else 0
            row_name = version+':'+file['file']+':'+str(line['line_number'])
            row_data.append([
                row_name, cov_result
            ])
        
        per_version_dict[full_file_name]['col_data'] = col_data
        per_version_dict[full_file_name]['row_data'] = row_data
    return per_version_dict

def add_next_spectra(per_version_dict, cov_json, tc_id, version):
    for file in cov_json['files']:
        full_file_name = version+'.'+file['file']
        assert full_file_name in per_version_dict.keys()

        per_version_dict[full_file_name]['col_data'].append(tc_id)

        for i in range(len(file['lines'])):
            line = file['lines'][i]
            lineNo = version+':'+file['file']+':'+str(line['line_number'])
            assert lineNo == per_version_dict[full_file_name]['row_data'][i][0]

            cov_result = 1 if line['count'] > 0 else 0

            per_version_dict[full_file_name]['row_data'][i].append(cov_result)
    return per_version_dict

# 1. remove all gcda files
# 2. execute test case
# 3. generate coverage json (line)
# 4. save to DB
# 5. writer spectra data in DB to csv
def spectra_data(db, tf, tp):
    tc_names = tf+tp

    version_list = xx.get_list_versions()

    tot_version_dict = []
    for version in version_list:
        version_num = int(version[3:])
        xx.build_version(version_num, onlyProject=True)

        per_version_dict = {}
        db.first = True
        for tc_name in tc_names:
            tc_id  = db.name2id[tc_name]

            xx.remove_all_gcda()
            xx.run_by_tc_name(tc_name)
            json_file_path = xx.generate_json_for_TC(tc_id, 'out.json')

            cov_json = rr.get_json_from_file_path(json_file_path)

            if db.first:
                per_version_dict = add_first_spectra(per_version_dict, cov_json, tc_id, version)
                db.first = False
            else:
                per_version_dict = add_next_spectra(per_version_dict, cov_json, tc_id, version)
        
        ww.write_spectra_data_to_csv(per_version_dict)
        tot_version_dict.append(per_version_dict)
    
    # db.cov_per_file['all'] = {}
    # db.first = True
    # for single_version in tot_version_dict:
    #     if db.first:
    #         first_file = list(single_version.keys())[0]
    #         db.cov_per_file['all']['col_data'] = single_version[first_file]['col_data']

    #         db.cov_per_file['all']['row_data'] = []
    #         for file in single_version.keys():
    #             file_data = single_version[file]
    #             db.cov_per_file['all']['row_data'] += file_data['row_data']

    #         db.first = False
    #     else:
    #        for file in single_version.keys():
    #            file_data = single_version[file]
    #            db.cov_per_file['all']['row_data'] += file_data['row_data']
    
    # spectra_data = db.cov_per_file
    # spectra_file = ww.write_spectra_data_to_csv(spectra_data)
    
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

def criteria_per_BUG(db, bugs):

    # per fails
    for bug in bugs.keys():
        bug_name = bug
        bug_id = db.name2id[bug_name]

        failing_file = bugs[bug]['file']
        failing_func = bugs[bug]['function']
        failing_line = bugs[bug]['line']

        row_data = [
            ['bug-file'],
            ['bug-func'],
            ['bug-line']
        ]
        col_data = ['criteria']

        execs_buggy_file_cnt = 0
        execs_buggy_func_cnt = 0
        execs_buggy_line_cnt = 0
        # per test case
        for tc_id in db.tc.keys():
            col_data.append(tc_id)


            tc_name = db.tc[tc_id]['name']
            print(bug_id, tc_name)
            if xx.run_needed(tc_id, 'summary'):
                xx.remove_all_gcda()
                xx.run_by_tc_name(tc_name)

            # for file criteria
            summ_path = xx.generate_summary_json_for_TC(tc_id)
            summ_json = rr.get_json_from_file_path(summ_path)

            execs_buggy_file= False
            for file in summ_json['files']:
                line_cov = file['line_covered']
                file_name = file['filename']

                if line_cov > 0 and check(file_name, failing_file):
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

                    if func_cov > 0 and check((file_name, func_name), failing_func):
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

                    if line_cov > 0 and check((file_name, line_no), failing_line):
                        execs_buggy_line = True
                        execs_buggy_line_cnt += 1
                        break
                
                if execs_buggy_line:
                    break
            
            row_data[2].append(int(execs_buggy_line))
            print("* {} on fail line".format(execs_buggy_line))

        db.tc_criteria['target'] = 'bug.'+bug_id
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

def processed_data(target_file):
    spectra_df = rr.get_csv_as_pandas_file_path(target_file)