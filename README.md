# gen_data_4_jsoncpp

```
./build.py --project jsoncpp --bug_version bug1 --withPreprocessed
./gen_data.py --project jsoncpp --bug_version bug1 --run_all_testcases
./gen_data.py --project jsoncpp --bug_version bug1 --spectrum_data
./gen_data.py --project jsoncpp --bug_version bug1 --processed_data
./gen_data.py --project jsoncpp --bug_version bug1 --ranked_data
```

## ToDo
* make PPT slides to share results
* analyze ossfuzz timeout bugs

## Currently Working On:
3. Change to execute for single BUG version (for simplicity)
4. documentation in GREAT DETAIL
* [IMPO] Check whether skipping TC runs are correctly skipped

## Finished Over the Week
* make different versions for each bug
  * make it buildable/executable for each bug
* generate coverage data on each version with all TC
* calculate suspicious score on each line using SBFL formulas
* utilized clang to retreive line-to-method data
  * currently does not handle lines that are not within a method
  * currently does not handle template functions
* Finished Ranking at Method Level (per SBFL Formula on each BUG)
* generate summary of acc@10 results at method level
* debug rank results
* improve performance on FL (by excluding coincident passed TC)

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

## TC-to-TC Relation Data
Shows ```<# of lines, # of functions, # of files>``` intersection on all TC-to-TC.

## Example Command
```
./gen_data.py --spectra_data --criteria_data --relation_data --list_tc --summary_json 1 --html 1 --pretty_json 1
```

## Command Line Interface
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
