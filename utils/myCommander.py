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

            db.cov_per_file[full_file_name]['col_data'].append(tc_id)

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
    ww.write_test_cases_list_to_txt(db.tc)
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
# 3. generate summary coverage json (file)
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
