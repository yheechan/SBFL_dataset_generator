import subprocess as sp
from pathlib import Path
import os
import csv
from . import myHelper as hh
import json

script_path = Path(os.path.realpath(__file__))
util_dir = script_path.parent
tool_dir = util_dir.parent
bin_dir = tool_dir.parent
main_dir = bin_dir.parent
src_dir = main_dir / 'src'
subjects_dir = main_dir / 'subjects'

def write_spectra_data_to_csv(project_name, spectra_data_per_file: dict):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    spectra_dir = data_dir / 'spectra'
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

def write_test_cases_list_to_txt(project_path, tc_list: list, pp=False):
    data_dir = project_path / 'data'
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

def write_TC_on_criteria_to_csv(project_path, criteria_data: dict):
    data_dir = project_path / 'data'
    crit_dir = data_dir / 'criteria'
    hh.check_dir(data_dir)
    hh.check_dir(crit_dir)

    file = crit_dir / 'criteria.csv'

    col_data = criteria_data['col_data']
    row_data = criteria_data['row_data']

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(col_data)
        cw.writerows(row_data)

def write_TC_on_criteria_per_BUG_to_csv(project_name, criteria_data: dict):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    crit_dir = data_dir / 'criteria'
    hh.check_dir(data_dir)
    hh.check_dir(crit_dir)

    file_name = criteria_data['target'] + '.csv'
    file = crit_dir / file_name

    col_data = criteria_data['col_data']
    row_data = criteria_data['row_data']

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(col_data)
        cw.writerows(row_data)

def write_criteria_stat_results_per_BUG_to_csv(project_name, cd, tot):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    crit_dir = data_dir / 'criteria'
    hh.check_dir(data_dir)
    hh.check_dir(crit_dir)

    file_name = cd['target'] + '.stats.csv'
    file = crit_dir / file_name

    xF_file = cd['xx_fail_file']
    nF_file = tot-(xF_file[0] + xF_file[1])
    xF_func = cd['xx_fail_func']
    nF_func = tot-(xF_func[0] + xF_func[1])
    xF_line = cd['xx_fail_line']
    nF_line = tot-(xF_line[0] + xF_line[1])

    col_data = ['criteria', 'executes&pass', 'executes&fail', 'not-executes', 'total']
    # (pass, fail)
    row_data = [
        ['buggy-file', xF_file[0], xF_file[1], nF_file, tot],
        ['buggy-func', xF_func[0], xF_func[1], nF_func, tot],
        ['buggy-line', xF_line[0], xF_line[1], nF_line, tot]
    ]

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(col_data)
        cw.writerows(row_data)

def write_criteria_stat_results_to_csv(project_path, cd, tot):
    data_dir = project_path / 'data'
    crit_dir = data_dir / 'criteria'
    hh.check_dir(data_dir)
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

def dump_dict_as_json(project_path, data):
    data_dir = project_path / 'data'
    hh.check_dir(data_dir)

    file = data_dir / 'cov_dump.json'

    with open(file, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)

def write_data_to_csv(project_path, data, file_name):
    data_dir = project_path / 'data'
    relation_dir = data_dir / 'relation'
    hh.check_dir(data_dir)
    hh.check_dir(relation_dir)

    full_name = file_name+'.csv'
    file = relation_dir / full_name

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(data['col_data'])
        cw.writerows(data['row_data'])

def write_df_to_csv(project_name, df, file_name):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    processed_dir = data_dir / 'processed'
    hh.check_dir(data_dir)
    hh.check_dir(processed_dir)

    csv_file_path = processed_dir / file_name
    df.to_csv(csv_file_path)

def write_line2function(project_path, data, bug_version):
    data_dir = project_path / 'data'
    line2function_dir = data_dir / 'line2function'
    hh.check_dir(data_dir)
    hh.check_dir(line2function_dir)

    file_name = bug_version+'.line2function.json'

    file = line2function_dir / file_name

    with open(file, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)

    
def write_ranked_data_to_csv(project_name, df, fname, level):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    rank_name = 'ranked-'+level
    ranked_dir = data_dir / rank_name
    hh.check_dir(data_dir)
    hh.check_dir(ranked_dir)

    file_name = fname+'.csv'
    file = ranked_dir / file_name

    df.to_csv(file)

def write_ranked_summary_to_csv(project_name, data, level):
    project = project_name.split('-')[0]
    bug_version = project_name.split('-')[1]
    
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    ranked_name = 'ranked-'+level
    ranked_dir = data_dir / ranked_name
    summary_dir = data_dir / 'summary'
    hh.check_dir(data_dir)
    hh.check_dir(ranked_dir)
    hh.check_dir(summary_dir)

    file_name = bug_version + '.rank.summary.csv'
    file = summary_dir / file_name

    with open(file, 'w') as fp:
        cw = csv.writer(fp)
        cw.writerow(data['col_data'])
        cw.writerows(data['row_data'])

def write_coincident_TC(project_name, bug_name, data):
    project_path = subjects_dir / project_name
    data_dir = project_path / 'data'
    coverage_dir = data_dir / 'coverage'
    coincident_dir = coverage_dir / 'coincident'
    hh.check_dir(data_dir)
    hh.check_dir(coverage_dir)
    hh.check_dir(coincident_dir)

    file_name = bug_name + '.coincidentTC.txt'
    file_path = coincident_dir / file_name

    with open(file_path, 'w') as fp:
        for d in data:
            tc_id = str(d[0])
            tc_name = str(d[1])
            line = tc_id + '#' + tc_name + '\n'
            fp.write(line)
