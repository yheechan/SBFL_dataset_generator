# SBFL_dataset_generator

## 1. 소개
해당 github 저장소에서 개발 된 도구는 Spectrum-Based Fault Localization (SBFL)을 위해 **스펙트럼 기반 특징 데이터셋**을 생성한다.
현재 [JsonCPP](https://github.com/open-source-parsers/jsoncpp) 오픈 소스 프로젝트의 총 **4가지 버전**에만 적용된다.
또한, 각 버전에는 **하나의 고유한 버그**가 존재한다.

## 2. Github 저장소로부터 도구 다운로드 방법
* Github 저장소 링크: https://github.com/yheechan/gen_data_4_jsoncpp.git
* 다운로드 명령어: 
  ```
  $ git clone https://github.com/yheechan/gen_data_4_jsoncpp.git
  ```
*  Git 설치 방법: [git 설치 방법 링크](https://git-scm.com/book/ko/v2/%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-Git-%EC%84%A4%EC%B9%98)

### 도구 다운로드 디렉토리 구조
```
SBFL_dataset_generator/
├─ README.md
├─ bin/
├─ docs/
└─ src/
```

## 3. 의존 도구 (Prerequisites)
1. Clang/LLVM
    * 버전: 13.0.1
    * 설치 방법 링크: https://apt.llvm.org/
    * 설치 명령어:
        ```
        $ wget https:/apt.llvm.org/llvm.sh
        $ chmod +x llvm.sh
        $ sudo ./llvm.sh 13 all
        ```
    * 환경 설정 필요

2. Gcovr
    * 설치 방법 링크: https://gcovr.com/en/stable/installation.html
    * 설치 명령어:
      ```
      $ pip install gcovr==6.0
      ```

3. Python Modules
    * Pandas 버전: 1.1.15
    * Numpy 버전: 1.19.5
    * 설치 명령어:
      ```
      $ pip install pandas==1.15 numpy==1.19.5
      ```

4. Make
    * 버전: 4.1

**참고 사항:** 개발 된 도구는 위 명시 되어있는 의존 도구들의 버전으로 개발 되었으며, 다른 버전으로 테스트 되지 않았습니다.

## 4. 구조 (5개 단계)

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
# 1. Downloads JsonCPP -> Switch to correct version -> Generate line2function data & TC executables
./build.py --project jsoncpp --bug_version bug1 --withPreprocessed

# 2. Runs all TC one by one, saving coverage information
./gen_data.py --project jsoncpp --bug_version bug1 --run_all_testcases

# 3. Post-Processes coverage information
./gen_data.py --project jsoncpp --bug_version bug1 --spectrum_data

# 4. Calculate spectrum-based informations from the coverage data
./gen_data.py --project jsoncpp --bug_version bug1 --processed_data

# 5. Assigns ranks according to suspicious score from SBFL formulas at function level
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

Generate Spectrum-Based Dataset.

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
