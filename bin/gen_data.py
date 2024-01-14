#!/usr/bin/python3
from utils import myCommander as cc
from utils import myDatabase as dd
from utils import myArgparser as pp

failing_info = {
    'failing_file': [
        'src/lib_json/json_value.cpp',
        'src/lib_json/json_reader.cpp'
    ],
    'failing_func': [
        (
            'src/lib_json/json_value.cpp',
            'Json::Value::resize(unsigned int)'
        ),
        (
            'src/lib_json/json_reader.cpp',
            'Json::Reader::readObject(Json::Reader::Token&)'
        ),
        (
            'src/lib_json/json_reader.cpp',
            'Json::OurReader::skipBom(bool)'
        ),
        (
            'src/lib_json/json_reader.cpp',
            'Json::OurReader::decodeNumber(Json::OurReader::Token&, Json::Value&)'
        )
    ],
    'failing_line': [
        ('src/lib_json/json_value.cpp', 915),
        ('src/lib_json/json_reader.cpp', 467),
        ('src/lib_json/json_reader.cpp', 1279),
        ('src/lib_json/json_reader.cpp', 1628)
    ],
}

fails = {
    'bug1': {
        'file': 'src/lib_json/json_value.cpp',
        'function': (
            'src/lib_json/json_value.cpp',
            'Json::Value::resize(unsigned int)'
        ),
        'line': ('src/lib_json/json_value.cpp', 915),
    },
    'bug2': {
        'file': 'src/lib_json/json_reader.cpp',
        'function': (
            'src/lib_json/json_reader.cpp',
            'Json::Reader::readObject(Json::Reader::Token&)'
        ),
        'line': ('src/lib_json/json_reader.cpp', 467),
    },
    'bug3': {
        'file': 'src/lib_json/json_reader.cpp',
        'function': (
            'src/lib_json/json_reader.cpp',
            'Json::OurReader::skipBom(bool)'
        ),
        'line': ('src/lib_json/json_reader.cpp', 1279),
    },
    'bug4': {
        'file': 'src/lib_json/json_reader.cpp',
        'function': (
            'src/lib_json/json_reader.cpp',
            'Json::OurReader::decodeNumber(Json::OurReader::Token&, Json::Value&)'
        ),
        'line': ('src/lib_json/json_reader.cpp', 1628),
    }
}

failing_per_bug = {
    'bug1': [
        'ValueTest/issue1264_1',
        'ValueTest/issue1264_2',
        'ValueTest/issue1264_3',
    ],
    'bug2': [
        'ReaderTest/allowNumericKeysTest_1',
        'ReaderTest/allowNumericKeysTest_2',
        'ReaderTest/allowNumericKeysTest_3',
    ],
    'bug3': [
        'CharReaderTest/ossFuzz_21916_1',
        'CharReaderTest/ossFuzz_21916_2',
        'CharReaderTest/ossFuzz_21916_3',
    ],
    'bug4': [
        'CharReaderTest/ossFuzz_18147_1',
        'CharReaderTest/ossFuzz_18147_2',
        'CharReaderTest/ossFuzz_18147_3',
    ]
}

tf = [
    'ValueTest/issue1264_1',
    'ValueTest/issue1264_2',
    'ValueTest/issue1264_3',
    'ReaderTest/allowNumericKeysTest_1',
    'ReaderTest/allowNumericKeysTest_2',
    'ReaderTest/allowNumericKeysTest_3',
    'CharReaderTest/ossFuzz_21916_1',
    'CharReaderTest/ossFuzz_21916_2',
    'CharReaderTest/ossFuzz_21916_3',
    'CharReaderTest/ossFuzz_18147_1',
    'CharReaderTest/ossFuzz_18147_2',
    'CharReaderTest/ossFuzz_18147_3',
]

tp = [
    'ValueTest/resizeArray',
    'ValueTest/checkNormalizeFloatingPointStr',
    'CharReaderFailIfExtraTest/issue107',
    'ReaderTest/parseWithNoErrors',
    'ValueTest/arrays',
    'StyledWriterTest/writeNestedObjects',
    'CharReaderTest/parseWithNoErrorsTestingOffsets',
    'ValueTest/memberCount',
    'ValueTest/offsetAccessors',
    'CharReaderTest/parseWithNoErrors',
    'ValueTest/objects',
    'ValueTest/StaticString'
]

if __name__ == "__main__":
    parser = pp.make_parser()
    args = parser.parse_args()
    
    project_name = args.project + '-' + args.bug_version

    db = dd.myDatabase()
    cc.assign_test_cases(project_name, db, tf)

    sd = (0, '')
    psd = (0, '')
    rd = (0, '')
    ct = (0, '')
    cb = (0, '')
    rt = (0, '')
    lt = (0, '')
    st = (0, '')
    ht = (0, '')
    pt = (0, '')

    if args.spectra_data:
        sd = cc.spectra_data(project_name, db, tf, tp, args.processed_data, failing_per_bug, fails)
    if args.processed_data:
        psd = cc.processed_data(project_name, db, failing_per_bug, fails)
    if args.ranked_data:
        rd = cc.ranked_data(project_name, db, failing_per_bug, fails)
    if args.criteria_data:
        ct = cc.criteria_all_TC(db, failing_info)
    if args.criteria_per_BUG:
        cb = cc.criteria_per_BUG(project_name, db, fails, failing_per_bug)
    if args.relation_data:
        rt = cc.relation_all_TC(db)
    if args.list_tc:
        lt = cc.list_test_cases(db, tf)
    if args.summary_json is not None:
        st = cc.summary_coverage_json_target_TC(db, args.summary_json)
    if args.html is not None:
        ht = cc.html_target_TC(db, args.html)
    if args.pretty_json is not None:
        pt = cc.pretty_json_TC(db, args.pretty_json)
    
    print()
    print()
    print("************************************")
    print("***** FINAL RESULTS ON COMMAND *****")
    print("************************************")

    if sd[0]:
        print(sd[1])
    if psd[0]:
        print(psd[1])
    if rd[0]:
        print(rd[1])
    if ct[0]:
        print(ct[1])
    if cb[0]:
        print(cb[1])
    if rt[0]:
        print(rt[1])
    if lt[0]:
        print(lt[1])
    if st[0]:
        print(st[1])
    if ht[0]:
        print(ht[1])
    if pt[0]:
        print(pt[1])
