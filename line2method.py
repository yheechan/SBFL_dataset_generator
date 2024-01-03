#!/usr/bin/python3
from utils import myExecutor as xx

if __name__ == "__main__":
    ii_files = xx.get_ii_files()
    print('ii_files: ')
    for file in ii_files:
        print(file)

    cpp_files = xx.change_ii_to_cpp(ii_files)
    print('cpp_files: ')
    for file in cpp_files:
        print(file)

    xx.extract_line2method(cpp_files)
