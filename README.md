# gen_data_4_jsoncpp

This programs generate ranked dataset for Spectrum-Based Fault Localization (SBFL).
Current limit is that it is limited to only [JsonCPP](https://github.com/open-source-parsers/jsoncpp).

## Dependencies
1. Clang/LLVM, version 13.0.1
  * apt package downloader: https://apt.llvm.org/
  * manually built from source: https://releases.llvm.org/download.html
    * ```sudo apt install llvm-13-dev clang-13 libclang-13-dev lld-13 libc++abi-13-dev```

2. Gcovr, version 6.0
  * install guide: https://gcovr.com/en/stable/installation.html

3. Python Modules
  * Pandas (1.1.15)
  * Numpy (1.19.5)

## EASY command for execution
```
# Generates SBFL dataset for all 4 bug versions of JsonCPP
./bin/SBFL_all.sh

# or

# Generates SBFL dataset for a single bug version of JsonCPP
./bin/SBFL_<bug-version>.sh
```

## Step-by-Step command execution (example)

```
./build.py --project jsoncpp --bug_version bug1 --withPreprocessed
./gen_data.py --project jsoncpp --bug_version bug1 --run_all_testcases
./gen_data.py --project jsoncpp --bug_version bug1 --spectrum_data
./gen_data.py --project jsoncpp --bug_version bug1 --processed_data
./gen_data.py --project jsoncpp --bug_version bug1 --ranked_data
```

## ToDo
* analyze ossfuzz timeout bugs

## TC Criteria
TC that:
  1. Not executes **cpp file** containing buggy line
  2. executes **cpp file** containing buggy line
  3. Not executes **class** containing buggy line
  4. executes **class** containing buggy line
  5. Not executes **function** containing buggy line
  6. executes **function** containing buggy line
  7. NOT executes buggy **lines**
  8. executes buggy **lines**

## Command Line Interface for ```./bin/gen_data.py```
```
usage: gen_data.py [-h] --project PROJECT --bug_version BUG_VERSION
                   [--run_all_testcases] [--spectrum_data] [--processed_data]
                   [--ranked_data]

Generate Spectrum-Based Data.

optional arguments:
  -h, --help            show this help message and exit

  --project PROJECT     project name (ex. jsoncpp)
  
  --bug_version BUG_VERSION
                        bug version (ex. bug1)
                        
  --run_all_testcases   Command that runs all existinc test cases. For each
                        run, it saves coverage result data
                        ('/<project>/data/coverage/'). It also generates lists
                        of test cases that coincidentally pass even when
                        running the buggy line
                        ('/<project>/data/coverage/coincident/<bug-
                        version>.coincidentTC.txt')

  --spectrum_data       Command that generates spectrum data on each file of
                        project from the test case coverage results.
                        ('<project>/data/spectra/')

  --processed_data      Command that processes the spectrum data (ep, ef, np,
                        nf) then running all the SBFL formula with the
                        processed data. The processed data is saved in
                        ('/<project>/data/processed/').

  --ranked_data         Command that ranks each method in standard of each
                        SBFL formula independantly using processed data. The
                        ranked data is saved in ('/<project>/data/ranked/').
                        It also generates a summary of the rank of the buggy
                        method on each SBFL formula
                        ('/<project>/data/ranked/<bug-
                        version>.rank.summary.csv').
```
