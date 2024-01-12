#!/usr/bin/python3
from utils import myExecutor as xx

if __name__ == "__main__":
    xx.build_ii()

    ii_files = xx.get_ii_files()
    print('ii_files: ')
    for file in ii_files:
        print(file)

    cpp_files = xx.change_ii_to_cpp(ii_files)
    print('cpp_files: ')
    for i in range(len(cpp_files)):
        print(i, '\t', cpp_files[i])

    xx.extract_line2method(cpp_files)
