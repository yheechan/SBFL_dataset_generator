#!/usr/bin/python3
import json
import csv
import subprocess as sp
import argparse
import os
from pathlib import Path

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent
main_dir = bin_dir.parent
test_dir = main_dir / 'build-1/src/test_lib_json'
data_dir = main_dir / 'data'
coverage_dir = main_dir / 'coverage'

failing_file = [
    'src/lib_json/json_reader.cpp',
    'src/lib_json/json_value.cpp'
]

failing_line = [
    (
        'src/lib_json/json_reader.cpp',
        'Json::OurReader::decodeNumber(Json::OurReader::Token&, Json::Value&)'
    ),
    (
        'src/lib_json/json_reader.cpp',
        'Json::OurReader::skipBom(bool)'
    ),
    (
        'src/lib_json/json_reader.cpp',
        "Json::Reader::readObject(Json::Reader::Token&)"
    ),
    (
        'src/lib_json/json_value.cpp',
        'Json::Value::resize(unsigned int)'
    )
]

failing_line = [
    ('src/lib_json/json_reader.cpp', 467),
    ('src/lib_json/json_reader.cpp', 1279),
    ('src/lib_json/json_reader.cpp', 1630),
    ('src/lib_json/json_value.cpp', 915)
]


failing_tc = [
    'CharReaderTest/failingTestCaseIntegerOverflows',
    'CharReaderTest/failingTestCaseHeapOverflows',
    'ReaderTest/allowNumericKeysTest',
    'ValueTest/resizePopulatesAllMissingElements'
]

passing_tc = [
    'CharReaderTest/parseWithNoErrors',
    'FastWriterTest/writeArrays',
    'StyledWriterTest/multiLineArray',
    'StyledStreamWriterTest/writeNumericValue',
    'StyledStreamWriterTest/writeArrays',
    'ReaderTest/parseString'
]

class CoverageData:
    def __init__(self):
        self.first = True

        # a dict with keys as file
        # a file holding info of cov per TC
        self.cov_per_file = {}

        # holds all TC information
        self.test_cases = {}
        self.tc2id = {}

        # info of counts on TC
        self.tc_cnt = 0
        self.fail_cnt = 0
        self.pass_cnt = 0

        self.tc_criterion = {}
        self.tc_relation = {}
    
    def get_json(self, json_data):
        json_file = coverage_dir / json_data
        cov_json = {}
        with open(json_file, 'r') as fp:
            cov_json = json.load(fp)
        return cov_json
    
    def get_summ_json(self, file):
        sum_json = {}
        with open(file, 'r') as fp:
            sum_json = json.load(fp)
        return sum_json
    
    def init_data(self, json_data, tc_name):
        cov_json = self.get_json(json_data)

        for file in cov_json["files"]:
            tc_id = self.tc2id[tc_name]
            col_data = ['lineNo', tc_id]
            row_data = []

            full_file_nm = file["file"]
            file_name = full_file_nm.split('/')[-1]

            if not full_file_nm in self.cov_per_file.keys():
                self.cov_per_file[full_file_nm] = {}

            for line in file["lines"]:
                cov_result = 1 if line["count"] > 0 else 0
                row_data.append([
                    line["line_number"], cov_result
                ])
            
            self.cov_per_file[full_file_nm]["col_data"] = col_data
            self.cov_per_file[full_file_nm]["row_data"] = row_data

    def add_data(self, json_data, tc_name):
        cov_json = self.get_json(json_data)

        for file in cov_json["files"]:
            full_file_nm = file["file"]
            file_name = full_file_nm.split('/')[-1]
            tc_id = self.tc2id[tc_name]

            self.cov_per_file[full_file_nm]["col_data"].append(tc_id)

            for i in range(len(file["lines"])):
                cov_result = 1 if file["lines"][i]["count"] > 0 else 0
                lineNo = file["lines"][i]["line_number"]

                assert(lineNo == self.cov_per_file[full_file_nm]["row_data"][i][0])

                self.cov_per_file[full_file_nm]["row_data"][i].append(cov_result)
    
    def file_criterion(self, tc_name):
        tc_id = self.tc2id[tc_name]
        summ_file = coverage_summary(tc_id)
        summ_json = self.get_summ_json(summ_file)

        for file in summ_json["files"]:
            col_data = ''
        print(len(summ_json))
        print(summ_json["branch_total"])
        pass
    
    def init_criterion(self, json_data, tc_name):
        tc_id = self.tc2id[tc_name]

        # file
        summ_file = coverage_summary(tc_id)
        summ_json = self.get_summ_json(summ_file)

        self.file_criterion(tc_name)
        pass
    
    def write_data(self):
        check_dir(data_dir)
        spectra_dir = data_dir / 'spectra'
        check_dir(spectra_dir)

        for file in self.cov_per_file.keys():
            file_nm_csv = file.replace('/', '.') + '.csv'
            col_data = self.cov_per_file[file]["col_data"]
            row_data = self.cov_per_file[file]["row_data"]

            file = spectra_dir / file_nm_csv
            with open(file, 'w') as fp:
                csv_writer = csv.writer(fp)
                csv_writer.writerow(col_data)
                csv_writer.writerows(row_data)
    
    def get_tc(self, pp=False):
        cmd = [
            './jsoncpp_test',
            '--list-tests'
        ]

        process = sp.Popen(
            cmd,
            stdout=sp.PIPE,
            stderr=sp.STDOUT, 
            cwd=test_dir,
            encoding="utf-8"
        )

        num = 1
        self.fail_cnt = 0
        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() != None:
                break

            id = 'TC' + str(num)
            name = line.strip()
            type = 'tp'

            if name in failing_tc:
                type = 'tf'
                self.fail_cnt += 1

            self.test_cases[id] = {
                'type': type,
                'test-case': name
            }
            self.tc2id[name] = id

            if pp:
                print('{}-{}: {}'.format(
                    id, type, name
                ))

            num += 1
        
        self.tc_cnt = len(self.test_cases.keys())
        self.pass_cnt = self.tc_cnt - self.fail_cnt
        print('>> got total {} TC\n\twith {} tf & {} tp'.format(
            self.tc_cnt, self.fail_cnt, self.pass_cnt
        ))
    
    def write_tc(self, file_nm):
        check_dir(data_dir)
        
        file = data_dir / file_nm
        with open(file, 'w') as fp:
            for tc in self.test_cases.keys():
                line = '{}-{}: {}\n'.format(
                    tc,
                    self.test_cases[tc]['type'],
                    self.test_cases[tc]['test-case'],
                )
                fp.write(line)

def gen_tc_list():
    covData = CoverageData()
    covData.get_tc(pp=True)
    file_nm = 'tc-list.txt'
    covData.write_tc(file_nm)
    print('>> completed writing list of test cases in {}'.format('data/'+file_nm))

def check_dir(dir):
    if not dir.exists():
        dir.mkdir()

def after_exec(res, statement):
    if res == 0:
        print(">> [SUCCESS] ",end='')
    else:
        print(">> [FAIL] ",end='')
    print(statement)

def remove_gcda():
    cmd = ['find', '.', '-type', 'f', '-name', '*.gcda', '-delete']
    sp.call(cmd)
    res = sp.call(cmd, cwd=main_dir)
    after_exec(res, "removing all *.gcda files")

def run_tc(tc_name):
    cmd = [
        './jsoncpp_test',
        '--test',
        tc_name
    ]
    res = sp.call(cmd, cwd=test_dir)
    after_exec(res, "running test case {}\n".format(tc_name))

def gen_json(output_name):
    check_dir(coverage_dir)
    
    output = coverage_dir / output_name
    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--json', output
    ]
    res = sp.call(cmd, cwd=main_dir)
    after_exec(res, "generating json coverage data using gcovr")

def gen_data(failing_tc, passing_tc):
    remove_gcda()
    testcases = failing_tc + passing_tc

    covData = CoverageData()
    covData.get_tc()

    json_name = 'out.json'
    for i in range(len(testcases)):
        tc_name = testcases[i]
        run_tc(tc_name)
        gen_json(json_name)

        if covData.first:
            covData.init_data(json_name, tc_name)
            covData.first = False
        else:
            covData.add_data(json_name, tc_name)
        
        remove_gcda()
    
    covData.write_data()

def gen_criterion():
    remove_gcda()
    covData = CoverageData()
    covData.get_tc()

    json_name = 'out.json'
    for tc_id in covData.test_cases.keys():
        tc_name = covData.test_cases[tc_id]['test-case']

        # run_tc(tc_name)
        # gen_json(json_name)

        if covData.first:
            covData.init_criterion(json_name, tc_name)
            covData.first = False
            break
        # else:
        #     covData.add_criterion(json_name, tc_name)
        
        remove_gcda()
    
    # covData.write_criterion()
    print("END!")

def coverage_summary(tc_id):
    check_dir(coverage_dir)

    covData = CoverageData()
    covData.get_tc()

    if tc_id not in covData.test_cases.keys():
        print('>> there is no test case {}'.format(tc_id))
        return
    
    summary_dir = coverage_dir / 'summary'
    check_dir(summary_dir)
    
    tc_name = covData.test_cases[tc_id]['test-case']
    
    file_name = tc_id + '.summary.json'
    output = summary_dir / file_name
    
    remove_gcda()
    run_tc(tc_name)
    
    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--json-summary-pretty', '--json', 'json-pretty',
        '-o', output
    ]
    res = sp.call(cmd, cwd=main_dir)
    after_exec(res, "generating json coverage summary data using gcovr")

    return output

def html(tc_id):
    covData = CoverageData()
    covData.get_tc()

    if tc_id not in covData.test_cases.keys():
        print('>> there is no test case {}'.format(tc_id))
        return
    
    tc_name = covData.test_cases[tc_id]['test-case']
    
    remove_gcda()
    run_tc(tc_name)

    check_dir(coverage_dir)
    
    html_dir = coverage_dir / 'html'
    check_dir(html_dir)
    
    tc_html_dir = html_dir / tc_id
    check_dir(tc_html_dir)

    html_file = tc_html_dir / 'cov.html'
    
    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--html', '--html-details',
        '-o', html_file,
        '-r', '.'
    ]

    res = sp.call(cmd, cwd=main_dir)

    after_exec(res, 'making html for coverage visualization')

def gen_html(tc_num):
    if tc_num is not None:
        tc_id = 'TC'+str(tc_num)
        html(tc_id)
    else:
        print('>> test case number not given.')
    

def print_summary(tc_num):
    if tc_num is not None:
        tc_id = 'TC'+str(tc_num)
        coverage_summary(tc_id)
    else:
        print('>> test case number not given.')

def coverage_pretty_print(tc_id):
    check_dir(coverage_dir)

    covData = CoverageData()
    covData.get_tc()

    if tc_id not in covData.test_cases.keys():
        print('>> there is no test case {}'.format(tc_id))
        return
    
    cov_pretty_dir = coverage_dir / 'cov_pretty'
    check_dir(cov_pretty_dir)

    tc_name = covData.test_cases[tc_id]['test-case']

    file_name = tc_id + '.pretty.json'
    output = cov_pretty_dir / file_name

    remove_gcda()
    run_tc(tc_name)

    cmd = [
        'gcovr',
        '--gcov-executable', 'llvm-cov gcov',
        '--json', '--json-pretty',
        '-o', output
    ]

    res = sp.call(cmd, cwd=main_dir)
    after_exec(res, "generating pretty json coverage summary data using gcovr")

def pretty_print(tc_num):
    if tc_num is not None:
        tc_id = 'TC'+str(tc_num)
        coverage_pretty_print(tc_id)
    else:
        print('>> test case number not given.')
    
def make_parser():
    parser = argparse.ArgumentParser(
        description='Generate Data.'
    )

    parser.add_argument(
        '--command',
        required=False,
        default='spectra-data',
        choices=[
            'spectra-data',
            'summary',
            'list-tc',
            'html',
            'pretty-json',
            'tc-criterion',
            'tc-relation'
        ],
        help='select which operation to run.'
    )

    parser.add_argument(
        '--tcNum',
        type=int,
        nargs='?',
        const=0,
        default=None,
        help='test case number (optional)')

    return parser

from utils import myCommander as cc
from utils import myDatabase as dd

if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    db = dd.myDatabase()
    cc.assign_test_cases(db, failing_tc)

    if args.command == 'spectra-data':
        cc.spectra_data(db, failing_tc, passing_tc)
    elif args.command == 'list-tc':
        cc.list_test_cases(db, failing_tc)
    elif args.command == 'summary':
        cc.summary_coverage_json_target_TC(db, args.tcNum)
        # print_summary(args.tcNum)
    elif args.command == 'html':
        gen_html(args.tcNum)
    elif args.command == 'pretty-json':
        pretty_print(args.tcNum)
    elif args.command == 'tc-criterion':
        gen_criterion()




