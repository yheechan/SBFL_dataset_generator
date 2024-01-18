# SBFL_dataset_generator

# 1. 소개
해당 github 저장소에서 개발 된 도구는 Spectrum-Based Fault Localization (SBFL)을 위해 **스펙트럼 기반 특징 데이터셋**을 생성한다.
현재 [JsonCPP](https://github.com/open-source-parsers/jsoncpp) 오픈 소스 프로젝트의 총 **4가지 버전**에만 적용된다.
또한, 각 버전에는 **하나의 고유한 버그**가 존재한다.

# 2. Github 저장소로부터 도구 다운로드 방법
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

**참고 사항:** 해당 문석에서 파일 경로 명시 할 때의 홈 디렉토리는 ```SBFL_dataset_generator/```로 가정합니다.

# 3. 의존 도구 (Prerequisites)
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

**참고 사항:** 현재 개발 된 도구는 위 명시 되어있는 의존 도구들의 버전으로 개발 되었으며, 다른 버전으로 테스트 되지 않았습니다.

# 4. 구조 (5개 단계)
![framwork](https://github.com/yheechan/gen_data_4_jsoncpp/blob/master/docs/img/framwork.png)
<그림 4.1> 개발 된 도구의 구조

### SBFL_dataset_generator/bin/ 디렉토리 구조 (사용자에게 제공 되는 명령어)
```
gen_data_4_jsoncpp/bin
├─ SBFL_all.sh
├─ SBFL_single.sh
├─ build_project.sh
├─ gen_processed.sh
├─ gen_spectrum.sh
├─ rank_functions.sh
├─ run_testcases.sh
└─ tools/
```

### ```<bug-version>```에 가능한 입력 값
* bug1
* bug2
* bug3
* bug4

### ```<bug-version>```의 입력 값을 ```bug1```기준, 단계 별 명령어 예제
작업 디렉토리를 ```SBFL_dataset_generator/bin/```으로 이동해서 실행한다:
```
$ ./build_project.sh bug1
$ ./run_testcases.sh bug1
$ ./gen_spectrum.sh bug1
$ ./gen_processed.sh bug1
$ ./rank_functions.sh bug1
```

**참고 사항:** 간편 실행은 [8장](google.com)에서 설명된다.

## 4.1 프로젝트 빌드 단계
![framwork-step1](https://github.com/yheechan/gen_data_4_jsoncpp/blob/master/docs/img/framwork-step1.png)

작업 디렉토리를 ```SBFL_dataset_generator/bin/```으로 이동해서 실행한다:
```
$ ./build_project.sh <bug-version>
```
* 해당 명령어를 실행하면 ```SBFL_dataset_generator/subjects/``` 디렉토리가 새롭게 생성된다. 
* ```<bug-version>```으로 입력 된 **jsoncpp 버전**의 프로젝트가 ```jsoncpp-<bug-version>/``` 이름으로 ```subjects/``` 디렉토리에 자동 저장 된다.
  * ```$ ./build_project.sh bug1``` 명령어를 실행 후 프로젝트 저장 결과
    ```
    gen_data_4_jsoncpp/
      └─subjects/
        └─ jsoncpp-bug1/
    ```
* 저장하게 된 jsoncpp 프로젝트는 **빌드** 되어 **jsoncpp executables**들이 생성 된다.
* jsoncpp의 소스 코드 전처리 파일들로부터 **line-function 정보**가 ```SBFL_dataset_generator/data/line2function/``` 디렉토리 위치에 ```<bug-version>.line2function.json```이름 형식으로 저장 된다.
  * ```$ ./build_project.sh bug1``` 명령어를 실행 후 **line-function 정보** 저장 결과
    ```
    gen_data_4_jsoncpp/subjects/jsoncpp-bug1/
      └─ data/
        └─ line2function/
          └─ bug1.line2function.json
    ```
* **line-function** 추출 정보 예시: ```<bug-version>.line2function.json```
  * 프로젝트의 소스 코드 **파일**의 **함수들의 이름**과 해당 함수의 **시작 지점**과 **끝나는 지점**을 json 포맷으로 저장한다
  ```
  {
    …
    “file1.cpp": [
      [“ClassA::foo(int x)”, 10, 15],
      [“ClassA::boo(int x)", 17, 24],
      …
    ],
    …
  }
  ```
