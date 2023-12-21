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

def add_first_spectra(db, cov_json, tc_id):
    for file in cov_json['files']:
        col_data = ['lineNo', tc_id]
        row_data = []

        full_file_name = file['file']

        if not full_file_name in db.cov_per_file.keys():
            db.cov_per_file[full_file_name] = {}
        
        for line in file['lines']:
            cov_result = 1 if line['count'] > 0 else 0
            row_data.append([
                line['line_number'], cov_result
            ])
        
        db.cov_per_file[full_file_name]['col_data'] = col_data
        db.cov_per_file[full_file_name]['row_data'] = row_data

def add_next_spectra(db, cov_json, tc_id):
    for file in cov_json['files']:
        full_file_name = file['file']
        assert full_file_name in db.cov_per_file.keys()

        db.cov_per_file[full_file_name]['col_data'].append(tc_id)

        for i in range(len(file['lines'])):
            line = file['lines'][i]
            lineNo = line['line_number']
            assert lineNo == db.cov_per_file[full_file_name]['row_data'][i][0]

            cov_result = 1 if line['count'] > 0 else 0

            db.cov_per_file[full_file_name]['row_data'][i].append(cov_result)

# 1. remove all gcda files
# 2. execute test case
# 3. generate coverage json (line)
# 4. save to DB
# 5. writer spectra data in DB to csv
def spectra_data(db, tf, tp):
    tc_names = tf+tp

    for tc_name in tc_names:
        tc_id  = db.name2id[tc_name]

        xx.remove_all_gcda()
        xx.run_by_tc_name(tc_name)
        json_file_path = xx.generate_json_for_TC(tc_id, 'out.json')

        cov_json = rr.get_json_from_file_path(json_file_path)

        if db.first:
            add_first_spectra(db, cov_json, tc_id)
            db.first = False
        else:
            add_next_spectra(db, cov_json, tc_id)
    
    spectra_data = db.cov_per_file
    ww.write_spectra_data_to_csv(spectra_data)
    
    print(">>> [COMPLETE] making spectra data for target TC")

# 1. executes './jsoncpp_test --list-tests' to gather list of TC
def list_test_cases(db, tf):
    ww.write_test_cases_list_to_txt(db.tc, pp=True)
    print(">>> [COMPLETE] writing test cases list to data/tc-list.txt")

# 1. remove all gcda files
# 2. execute test case
# 3. generate summary coverage json (file)
def summary_coverage_json_target_TC(db, num):
    if hh.check_num(num):
        tc_id = 'TC'+str(num)

        if not tc_id in db.tc.keys():
            print(">>> [IN-COMPLETE] test case doesn't exist: {}".format(tc_id))
            return

        tc_name = db.tc[tc_id]['name']

        xx.remove_all_gcda()
        xx.run_by_tc_name(tc_name)
        xx.generate_summary_json_for_TC(tc_id)
    else:
        print(">>> [IN-COMPLETE] test case number is not given")

# 1. remove all gcda files
# 2. execute test case
# 3. generate html
def html_target_TC(db, num):
    if hh.check_num(num):
        tc_id = 'TC'+str(num)

        if not tc_id in db.tc.keys():
            print(">>> [IN-COMPLETE] test case doesn't exist: {}".format(tc_id))
            return

        tc_name = db.tc[tc_id]['name']

        xx.remove_all_gcda()
        xx.run_by_tc_name(tc_name)
        xx.generate_html_for_TC(tc_id)
    else:
        print(">>> [IN-COMPLETE] test case number is not given")

# 1. remove all gcda files
# 2. execute test case
# 3. generate html
def pretty_json_TC(db, num):
    if hh.check_num(num):
        tc_id = 'TC'+str(num)

        if not tc_id in db.tc.keys():
            print(">>> [IN-COMPLETE] test case doesn't exist: {}".format(tc_id))
            return

        tc_name = db.tc[tc_id]['name']

        xx.remove_all_gcda()
        xx.run_by_tc_name(tc_name)
        xx.generate_pretty_json_for_TC(tc_id)
    else:
        print(">>> [IN-COMPLETE] test case number is not given")

def check_fail_file(name, fails):
    found = False
    if name in fails:
        found = True
    return found

def check_fail(file_name, specifics, failing):
    found = False
    for ff in failing:
        if file_name == ff[0] and specifics == ff[1]:
            found = True
            break
    return found

# Gen one csv containing 0 or 1 for all TC
def criterion_all_TC(db, failing_info):
    failing_file = failing_info['failing_file']
    failing_func = failing_info['failing_func']
    failing_line = failing_info['failing_line']

    row_data = [
        ['bug-file'],
        ['bug-func'],
        ['bug-line'],
    ]
    col_data = ['criterion']

    execs_buggy_file_cnt = 0
    execs_buggy_func_cnt = 0
    execs_buggy_line_cnt = 0
    for tc_id in db.tc.keys():
        col_data.append(tc_id)

        tc_name = db.tc[tc_id]['name']
        xx.remove_all_gcda()
        xx.run_by_tc_name(tc_name)

        # for file criterion
        summ_path = xx.generate_summary_json_for_TC(tc_id)
        summ_json = rr.get_json_from_file_path(summ_path)

        execs_buggy_file = False
        for file in summ_json['files']:
            line_cov = file['line_covered']
            file_name = file['filename']

            if line_cov > 0 and check_fail_file(file_name, failing_file):
                execs_buggy_file = True
                execs_buggy_file_cnt += 1
                break
            
        row_data[0].append(int(execs_buggy_file))
        print("* {} on fail file".format(execs_buggy_file))


        # for func criterion
        cov_path = xx.generate_json_for_TC(tc_id, 'out.json')
        cov_json = rr.get_json_from_file_path(cov_path)

        execs_buggy_func = False
        for file in cov_json['files']:
            file_name = file['file']
            for function in file['functions']:
                func_cov = function['execution_count']
                func_name = function['name']

                if func_cov > 0 and check_fail(
                    file_name, func_name, failing_func
                ):
                    execs_buggy_func = True
                    execs_buggy_func_cnt += 1
                    break
            
            if execs_buggy_func:
                break
        
        row_data[1].append(int(execs_buggy_func))
        print("* {} on fail func".format(execs_buggy_func))

        # for func criterion
        execs_buggy_line = False
        for file in cov_json['files']:
            file_name = file['file']
            for line in file['lines']:
                line_cov = line['count']
                line_no = line['line_number']

                if line_cov > 0 and check_fail(
                    file_name, line_no, failing_line
                ):
                    execs_buggy_line = True
                    execs_buggy_line_cnt += 1
                    break
            
            if execs_buggy_line:
                break
        
        row_data[2].append(int(execs_buggy_line))
        print("* {} on fail line".format(execs_buggy_line))
    
    db.tc_criterion['col_data'] = col_data
    db.tc_criterion['row_data'] = row_data
    db.tc_criterion['xx_fail_file'] = execs_buggy_file_cnt
    db.tc_criterion['xx_fail_func'] = execs_buggy_func_cnt
    db.tc_criterion['xx_fail_line'] = execs_buggy_line_cnt
    
    ww.write_TC_on_criterion_to_csv(db.tc_criterion)
    ww.write_criterion_stat_results(db.tc_criterion, db.tc_cnt)

    print(">>> [COMPLETE] making TC on criterion data for all TC")
