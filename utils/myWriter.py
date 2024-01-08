import subprocess as sp
from pathlib import Path
import os
import csv
from . import myHelper as hh
import json

script_path = Path(os.path.realpath(__file__))
util_dir = script_path.parent
bin_dir = util_dir.parent
main_dir = bin_dir.parent
test_dir = main_dir / 'build/src/test_lib_json'
data_dir = main_dir / 'data'
line2method_dir = data_dir / 'line2method'
coverage_dir = main_dir / 'coverage'
spectra_dir = data_dir / 'spectra'
tc_list_file = coverage_dir / 'tc-list.txt'
cov_pretty_dir = coverage_dir / 'cov_pretty'
html_dir = coverage_dir / 'html'
summary_dir = coverage_dir / 'summary'

def write_spectra_data_to_csv(spectra_data_per_file: dict):
    hh.check_dir(data_dir)
    hh.check_dir(spectra_dir)

    for file in spectra_data_per_file.keys():
        file_name = file.replace('/', '.') + '.csv'
        row_data = spectra_data_per_file[file]['row_data']
        col_data = spectra_data_per_file[file]['col_data']

        file = spectra_dir / file_name
        with open(file, 'w') as fp:
            cw = csv.writer(fp)
            cw.writerow(col_data)
            cw.writerows(row_data)
    
    return file

def write_test_cases_list_to_txt(tc_list: list, pp=False):
    hh.check_dir(data_dir)
    file = data_dir / 'tc-list.txt'
    with open(file, 'w') as fp:
        for tc in tc_list.keys():
            line = '{}-{}: {}'.format(
                tc, tc_list[tc]['type'],
                tc_list[tc]['name']
            )
            fp.write(line+'\n')

            if pp:
                print(line)

def write_TC_on_criteria_to_csv(criteria_data: dict):
    hh.check_dir(data_dir)
    crit_dir = data_dir / 'criteria'
    hh.check_dir(crit_dir)
    file = crit_dir / 'criteria.csv'

    col_data = criteria_data['col_data']
    row_data = criteria_data['row_data']

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(col_data)
        cw.writerows(row_data)

def write_TC_on_criteria_per_BUG_to_csv(criteria_data: dict):
    hh.check_dir(data_dir)
    crit_dir = data_dir / 'criteria-per-BUG'
    hh.check_dir(crit_dir)
    file_name = criteria_data['target'] + '.csv'
    file = crit_dir / file_name

    col_data = criteria_data['col_data']
    row_data = criteria_data['row_data']

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(col_data)
        cw.writerows(row_data)

def write_criteria_stat_results_per_BUG_to_csv(cd, tot):
    hh.check_dir(data_dir)
    crit_dir = data_dir / 'criteria-per-BUG'
    hh.check_dir(crit_dir)
    file_name = cd['target'] + '.stats.csv'
    file = crit_dir / file_name

    xF_file = cd['xx_fail_file']
    nF_file = tot-xF_file
    xF_func = cd['xx_fail_func']
    nF_func = tot-xF_func
    xF_line = cd['xx_fail_line']
    nF_line = tot-xF_line

    col_data = ['criteria', 'executes', 'not-executes', 'total']
    row_data = [
        ['buggy-file', xF_file, nF_file, tot],
        ['buggy-func', xF_func, nF_func, tot],
        ['buggy-line', xF_line, nF_line, tot]
    ]

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(col_data)
        cw.writerows(row_data)

def write_criteria_stat_results_to_csv(cd, tot):
    hh.check_dir(data_dir)
    crit_dir = data_dir / 'criteria'
    hh.check_dir(crit_dir)
    file = crit_dir / 'criteria_stats.csv'

    xF_file = cd['xx_fail_file']
    nF_file = tot-xF_file
    xF_func = cd['xx_fail_func']
    nF_func = tot-xF_func
    xF_line = cd['xx_fail_line']
    nF_line = tot-xF_line

    col_data = ['criteria', 'executes', 'not-executes', 'total']
    row_data = [
        ['buggy-file', xF_file, nF_file, tot],
        ['buggy-func', xF_func, nF_func, tot],
        ['buggy-line', xF_line, nF_line, tot]
    ]

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(col_data)
        cw.writerows(row_data)

def dump_dict_as_json(data):
    hh.check_dir(data_dir)
    file = data_dir / 'cov_dump.json'

    with open(file, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)

def write_data_to_csv(data, file_name):
    hh.check_dir(data_dir)
    relation_dir = data_dir / 'relation'
    hh.check_dir(relation_dir)

    full_name = file_name+'.csv'
    file = relation_dir / full_name

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(data['col_data'])
        cw.writerows(data['row_data'])

def write_df_to_csv(df, file_name):
    hh.check_dir(data_dir)
    processed_dir = data_dir / 'processed'
    hh.check_dir(processed_dir)

    csv_file_path = processed_dir / file_name
    df.to_csv(csv_file_path)

def write_line2method(data, bug_version):
    hh.check_dir(data_dir)
    hh.check_dir(line2method_dir)

    file_name = bug_version+'.line2method.json'

    file = line2method_dir / file_name

    with open(file, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
    
def write_ranked_data_to_csv(df, fname):
    hh.check_dir(data_dir)
    ranked_dir = data_dir / 'ranked'
    hh.check_dir(ranked_dir)

    file_name = fname+'.csv'
    file = ranked_dir / file_name

    df.to_csv(file)

def write_ranked_summary_to_csv(data):
    hh.check_dir(data_dir)
    ranked_dir = data_dir / 'ranked'
    hh.check_dir(ranked_dir)

    file_name = 'rank.summary.csv'
    file = ranked_dir / file_name

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(data['col_data'])
        cw.writerows(data['row_data'])
