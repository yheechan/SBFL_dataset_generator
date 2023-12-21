import argparse

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