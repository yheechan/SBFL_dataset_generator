import argparse

def make_parser():
    parser = argparse.ArgumentParser(
        description='Generate Spectrum-Based Dataset.'
    )

    parser.add_argument(
        '--project',
        type=str,
        required=True,
        help='project name (ex. jsoncpp)'
    )

    parser.add_argument(
        '--bug_version',
        type=str,
        required=True,
        help='bug version (ex. bug1)'
    )

    parser.add_argument(
        '--run_all_testcases',
        action='store_true',
        help='Command that runs all existinc test cases. \
                For each run, it saves coverage result data (\'/<project>/data/coverage/\').\
                It also generates lists of test cases that coincidentally\
                pass even when running the buggy line \
                (\'/<project>/data/coverage/coincident/<bug-version>.coincidentTC.txt\')'
    )

    parser.add_argument(
        '--spectrum_data',
        action='store_true',
        help='Command that generates spectrum data on each file of project \
                from the test case coverage results. \
                (\'<project>/data/spectra/\')'
    )

    # parser.add_argument(
    #     '--criteria_data',
    #     action='store_true',
    #     help='Generates CSV file for all TC to a criteria.'
    # )

    parser.add_argument(
        '--processed_data',
        action='store_true',
        help='Command that processes the spectrum data (ep, ef, np, nf) \
                then running all the SBFL formula with the processed data.\
                The processed data is saved in (\'/<project>/data/processed/\').'
    )

    parser.add_argument(
        '--ranked_data',
        action='store_true',
        help='Command that ranks each method in standard of each SBFL formula independantly \
                using processed data. \
                The ranked data is saved in (\'/<project>/data/ranked/\'). \
                It also generates a summary of the rank of the buggy method on each SBFL formula \
                (\'/<project>/data/ranked/<bug-version>.rank.summary.csv\').'
    )

    # parser.add_argument(
    #     '--relation_data',
    #     action='store_true',
    #     help='Generates TC-to-TC relation csv on per-file, per-function, per-line intersections.'
    # )

    # parser.add_argument(
    #     '--list_tc',
    #     action='store_true',
    #     help='Generates a text file containing the list of test cases.'
    # )

    # parser.add_argument(
    #     '--summary_json',
    #     type=int,
    #     default=None,
    #     help='Generates coverage summary in json format for a selected TC. (ex. --summary-json <tcNum>)'
    # )

    # parser.add_argument(
    #     '--html',
    #     type=int,
    #     default=None,
    #     help='Generates html of coverage data for a selected TC. (ex. --html <tcNum>)'
    # )

    # parser.add_argument(
    #     '--pretty_json',
    #     type=int,
    #     default=None,
    #     help='Generates coverage in pretty json format for a selected TC. (ex. --html <tcNum>)'
    # )

    return parser