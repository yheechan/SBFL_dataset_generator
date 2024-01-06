# gen_data_4_jsoncpp

## ToDo
* make different versions for each bug
  * make it buildable/executable for each bug
* generate coverage data on each version with all TC
* calculate supsicious score for all the lines on all versions
* analyze ossfuzz timeout bugs

## Currently Working On:
* make line2method dataset
* make acc@10 scores on method level
* [IMPO] Check whether skipping TC runs are correctly skipped

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
usage: gen_data.py [-h] [--spectra_data] [--criteria_data]
                   [--criteria_per_BUG] [--relation_data] [--list_tc]
                   [--summary_json SUMMARY_JSON] [--html HTML]
                   [--pretty_json PRETTY_JSON]

Generate Spectrum-Based Data.

optional arguments:
  -h, --help            show this help message and exit
  --spectra_data        Generates spectrum-based data with selected Failing &
                        Passing TC.
  --criteria_data       Generates CSV file for all TC to a criteria.
  --criteria_per_BUG    Generates CSV file for all TC to a criteria per BUG.
  --relation_data       Generates TC-to-TC relation csv on per-file, per-
                        function, per-line intersections.
  --list_tc             Generates a text file containing the list of test
                        cases.
  --summary_json SUMMARY_JSON
                        Generates coverage summary in json format for a
                        selected TC. (ex. --summary-json <tcNum>)
  --html HTML           Generates html of coverage data for a selected TC.
                        (ex. --html <tcNum>)
  --pretty_json PRETTY_JSON
                        Generates coverage in pretty json format for a
                        selected TC. (ex. --html <tcNum>)
```
