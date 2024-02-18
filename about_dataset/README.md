# SBFL 특징 데이터셋

# 1. 데이터셋 통계
* 총 버그 개수: **162개**
* 버그 출처
    출처 | 개수
    --- | ---
    ossfuzz | 2개
    github issue | 2개
    mutant based | 158개

# 2. 디렉토리 구조
데이터셋 세부 디렉토리 별 정보:
* ``overall/line2function``: 버그 버전 별 각 jsoncpp 소스 코드에 대한 **라인-함수 매핑 정보**
* ``overall/failing``: 버그 버전 별 **Failing 테스트 케이스 정보** (참고용으로 사용)
* ``overall/coverage``: 버그 버전 별 각 127 테스트 케이스에 대한 **JSON 형식 커버리지 정보**
* ``overall/spectra``: json 형식 커버리지 정보를 **CSV 형식으로 후처리 한 정보**
* ``overall/processed``: 버그 버전 별 각 jsoncpp 소스 코드에 대한 **SBFL 특징 계산 정보**
* ``overall/ranked-line``: 버그 버전 별 SBFL 특징 계산 정보 **(중요: 모델 학습 데이터로 사용)**

    ```
    overall/
      ├── line2function
      ├── failing
      ├── coverage
      ├── spectra
      ├── processed
      └── ranked-line
    ```

# 3. 각 버그 별 라인 정보

## ossfuzz와 github issue 버그 정보
index | 버기 버전 | 출처 | 소스 코드 파일  | buggy line # | bug type
--- | --- | --- | --- | --- | ---
1 | bug1 | [github issue #1253](https://github.com/open-source-parsers/jsoncpp/issues/1253) | json_value.cpp |  915 | Assertion Violation: Updated size of an array type
2 | bug2 | [github issue #1121](https://github.com/open-source-parsers/jsoncpp/issues/1121) | json_reader.cpp | 467 | Assertion Violation: Input type (expecting string Value)
3 | bug3 | [ossfuzz #18147](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=18147&q=jsoncpp&can=1&sort=-summary) | json_reader.cpp |  1279 | heap overflow
4 | bug4 | [ossfuzz #21916](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=21916&q=jsoncpp&can=1) | json_reader.cpp | 1628 | integer overflow

## Mutant based 버그 정보
index | 버그 버전 | 소스 코드 파일 | 라인 | operation | 변형 전 | 변형 후
--- | --- | --- | --- | --- | --- | ---
5 | json_reader.MUT14.cpp | json_reader.cpp | 70 | SRSR | features.strictRoot_ = true | return features;
6 | json_reader.MUT534.cpp | json_reader.cpp | 137 | VSCR | strictRoot_ | allowNumericKeys_
7 | json_reader.MUT577.cpp | json_reader.cpp | 142 | VLPR | token.start_ | endDoc
8 | json_reader.MUT634.cpp | json_reader.cpp | 150 | VGSR | successful | stackLimit_g
9 | json_reader.MUT701.cpp | json_reader.cpp | 166 | SRSR | this->currentValue().setComment(this->commentsBefore_ | return this->addError("Syntax error: value
10 | json_reader.MUT834.cpp | json_reader.cpp | 188 | SRSR | this->currentValue().setOffsetStart(token.start_ - this->begin_) | return successful;
11 | json_reader.MUT874.cpp | json_reader.cpp | 193 | SRSR | this->currentValue().swapPayload(v) | return this->addError("Syntax error: value
12 | json_reader.MUT953.cpp | json_reader.cpp | 201 | VSCR | end_ | start_
13 | json_reader.MUT1147.cpp | json_reader.cpp | 233 | SSDL | this->readToken(token) | ;
14 | json_reader.MUT1230.cpp | json_reader.cpp | 251 | SRSR | break; | return ok;
15 | json_reader.MUT1442.cpp | json_reader.cpp | 290 | CLCR | 3 | 56
16 | json_reader.MUT2214.cpp | json_reader.cpp | 377 | DirVarIncDec | begin | (++begin)
17 | json_reader.MUT2373.cpp | json_reader.cpp | 392 | CLCR | '/' | 1
18 | json_reader.MUT2551.cpp | json_reader.cpp | 416 | VLPR | this->end_ | p
19 | json_reader.MUT2720.cpp | json_reader.cpp | 425 | STRI | (this->current_ = p) < this->end_ | ((this->current_ = p) < this->end_) ? 1 : kill(getpid()
20 | json_reader.MUT2953.cpp | json_reader.cpp | 442 | VGSR | c | stackLimit_g
21 | json_reader.MUT2986.cpp | json_reader.cpp | 450 | ArgIncDec | token.start_ - this->begin_ | token.start_ - this->begin_-1
22 | json_reader.MUT3346.cpp | json_reader.cpp | 485 | OLBN | \|\| | &
23 | json_reader.MUT3350.cpp | json_reader.cpp | 486 | OLNG | (comma.type_ != tokenObjectEnd && comma.type_ != tokenArraySeparator && comma.type_ != tokenComment) | !((comma.type_ != tokenObjectEnd && comma.type_ != tokenArraySeparator && comma.type_ != tokenComment))
24 | json_reader.MUT3510.cpp | json_reader.cpp | 504 | VSCR | begin_ | end_
25 | json_reader.MUT3512.cpp | json_reader.cpp | 505 | SRSR | this->skipSpaces() | return true;
26 | json_reader.MUT3630.cpp | json_reader.cpp | 524 | SRSR | while (currentToken.type_ == tokenComment && ok) | return this->recoverFromError(tokenArrayEnd);
27 | json_reader.MUT3713.cpp | json_reader.cpp | 529 | CLSR | badTokenType | 0
28 | json_reader.MUT3809.cpp | json_reader.cpp | 544 | VSCR | start_ | end_
29 | json_reader.MUT4530.cpp | json_reader.cpp | 606 | FunCalDel | is >> value | 0
30 | json_reader.MUT4776.cpp | json_reader.cpp | 627 | CLCR | 1 | 2
31 | json_reader.MUT5361.cpp | json_reader.cpp | 668 | IndVarRepLoc | current | end
32 | json_reader.MUT5712.cpp | json_reader.cpp | 688 | OPPO | current++ | current--
33 | json_reader.MUT6007.cpp | json_reader.cpp | 706 | STRP | return this->addError("Bad unicode escape sequence in string: four digits expected." | kill(getpid()
34 | json_reader.MUT6049.cpp | json_reader.cpp | 710 | ORSN | < | >>
35 | json_reader.MUT6062.cpp | json_reader.cpp | 711 | DirVarLogNeg | *current++ | (!*current++)
36 | json_reader.MUT6179.cpp | json_reader.cpp | 715 | CLSR | c | 97
37 | json_reader.MUT6349.cpp | json_reader.cpp | 724 | IndVarRepReq | unicode | (1)
38 | json_reader.MUT6760.cpp | json_reader.cpp | 776 | ORAN | == | %
39 | json_reader.MUT7266.cpp | json_reader.cpp | 843 | ORLN | > | \|\|
40 | json_reader.MUT7297.cpp | json_reader.cpp | 844 | ORRN | > | !=
41 | json_reader.MUT7631.cpp | json_reader.cpp | 1019 | SRSR | this->lastValueEnd_ = nullptr | return false;
42 | json_reader.MUT8265.cpp | json_reader.cpp | 1106 | SSDL | break; | ;
43 | json_reader.MUT8538.cpp | json_reader.cpp | 1144 | VGSR | successful | stackLimit_g
44 | json_reader.MUT8824.cpp | json_reader.cpp | 1204 | VLSR | token.type_ | ok
45 | json_reader.MUT8963.cpp | json_reader.cpp | 1220 | OEAA | = | -=
46 | json_reader.MUT8997.cpp | json_reader.cpp | 1224 | OEAA | = | -=
47 | json_reader.MUT9114.cpp | json_reader.cpp | 1239 | STRP | if (this->features_.allowSpecialFloats_) { | kill(getpid()
48 | json_reader.MUT9300.cpp | json_reader.cpp | 1268 | CRCR | c | (-2147483648)
49 | json_reader.MUT9587.cpp | json_reader.cpp | 1293 | VSCR | current_ | lastValueEnd_
50 | json_reader.MUT9627.cpp | json_reader.cpp | 1303 | CLCR | '*' | 47
51 | json_reader.MUT9934.cpp | json_reader.cpp | 1338 | ORAN | == | *
52 | json_reader.MUT10330.cpp | json_reader.cpp | 1382 | CLCR | '\r' | 10
53 | json_reader.MUT10369.cpp | json_reader.cpp | 1387 | SBRC | break | continue
54 | json_reader.MUT10462.cpp | json_reader.cpp | 1399 | CGCR | '0' | 0
55 | json_reader.MUT10645.cpp | json_reader.cpp | 1407 | VSCR | end_ | lastValueEnd_
56 | json_reader.MUT10773.cpp | json_reader.cpp | 1413 | OCNG | (this->current_ = p) < this->end_ | !((this->current_ = p) < this->end_)
57 | json_reader.MUT10858.cpp | json_reader.cpp | 1415 | OPPO | p++ | p--
58 | json_reader.MUT11067.cpp | json_reader.cpp | 1440 | IndVarAriNeg | '\'' | (-'\'')
59 | json_reader.MUT11377.cpp | json_reader.cpp | 1471 | CGCR | 1U | 0
60 | json_reader.MUT11398.cpp | json_reader.cpp | 1473 | OCNG | this->features_.rejectDupKeys_ && this->currentValue().isMember(name) | !(this->features_.rejectDupKeys_ && this->currentValue().isMember(name))
61 | json_reader.MUT12345.cpp | json_reader.cpp | 1608 | OCNG | c < '0' \|\| c > '9' | !(c < '0' \|\| c > '9')
62 | json_reader.MUT12429.cpp | json_reader.cpp | 1612 | CLSR | value | 48
63 | json_reader.MUT12683.cpp | json_reader.cpp | 1629 | IndVarRepReq | 10 | (0x7fffffff)
64 | json_reader.MUT12996.cpp | json_reader.cpp | 1657 | IndVarRepReq | value | (-1.0)
65 | json_reader.MUT13246.cpp | json_reader.cpp | 1680 | CGCR | '\\' | 0
66 | json_reader.MUT14057.cpp | json_reader.cpp | 1736 | OCNG | *(current++) == '\\' && *(current++) == 'u' | !(*(current++) == '\\' && *(current++) == 'u')
67 | json_reader.MUT14345.cpp | json_reader.cpp | 1745 | IndVarRepPar | current | end
68 | json_reader.MUT14381.cpp | json_reader.cpp | 1753 | VLPR | current | end
69 | json_reader.MUT14425.cpp | json_reader.cpp | 1758 | SRSR | for (int index = 0; index < 4; ++index) { | return true;
70 | json_reader.MUT14472.cpp | json_reader.cpp | 1760 | SRSR | unicode *= 16 | return true;
71 | json_reader.MUT14512.cpp | json_reader.cpp | 1761 | OLNG | c <= '9' | !(c <= '9')
72 | json_reader.MUT14545.cpp | json_reader.cpp | 1762 | CLCR | '0' | 102
73 | json_reader.MUT14578.cpp | json_reader.cpp | 1763 | VLSR | c | index
74 | json_reader.MUT14591.cpp | json_reader.cpp | 1764 | OAAA | += | %=
75 | json_reader.MUT14661.cpp | json_reader.cpp | 1766 | OAAA | += | -=
76 | json_reader.MUT15097.cpp | json_reader.cpp | 1819 | ORBN | == | &
77 | json_reader.MUT15229.cpp | json_reader.cpp | 1831 | DirVarRepLoc | line | current
78 | json_reader.MUT15264.cpp | json_reader.cpp | 1836 | VLSR | line | column
79 | json_reader.MUT15481.cpp | json_reader.cpp | 1876 | DirVarIncDec | beginDoc | (++beginDoc)
80 | json_reader.MUT15567.cpp | json_reader.cpp | 1878 | FunCalDel | this->reader_.getFormattedErrorMessages() | 1
81 | json_reader.MUT15684.cpp | json_reader.cpp | 1895 | VSCR | allowSingleQuotes_ | strictRoot_
82 | json_reader.MUT16311.cpp | json_reader.cpp | 1961 | ArgRepReq | "allowComments" | (0)
83 | json_value.MUT43.cpp | json_value.cpp | 94 | CLSR | value | 1
84 | json_value.MUT94.cpp | json_value.cpp | 95 | DirVarLogNeg | value | (!value)
85 | json_value.MUT121.cpp | json_value.cpp | 99 | DirVarLogNeg | value | (!value)
86 | json_value.MUT148.cpp | json_value.cpp | 104 | ORRN | >= | !=
87 | json_value.MUT302.cpp | json_value.cpp | 126 | SRSR | memcpy(newString | return newString;
88 | json_value.MUT1214.cpp | json_value.cpp | 307 | VLSR | comp | other_len
89 | json_value.MUT1337.cpp | json_value.cpp | 319 | DirVarIncDec | other_len | (--other_len)
90 | json_value.MUT1358.cpp | json_value.cpp | 322 | ArgIncDec | other.cstr_ | other.cstr_+1
91 | json_value.MUT1991.cpp | json_value.cpp | 469 | VSCR | start_ | limit_
92 | json_value.MUT2004.cpp | json_value.cpp | 470 | VSCR | limit_ | start_
93 | json_value.MUT2026.cpp | json_value.cpp | 474 | DirVarRepExt | other | null
94 | json_value.MUT2066.cpp | json_value.cpp | 484 | IndVarAriNeg | 1 | (-1)
95 | json_value.MUT2195.cpp | json_value.cpp | 498 | ORRN | < | <=
96 | json_value.MUT2223.cpp | json_value.cpp | 500 | ORLN | < | \|\|
97 | json_value.MUT2342.cpp | json_value.cpp | 513 | SRSR | decodePrefixedString(this->isAllocated() | return this->value_.int_ < other.value_.int_;
98 | json_value.MUT2476.cpp | json_value.cpp | 520 | ORRN | < | >
99 | json_value.MUT2522.cpp | json_value.cpp | 524 | ORAN | < | +
100 | json_value.MUT2567.cpp | json_value.cpp | 530 | CLSR | thisSize | 0
101 | json_value.MUT2631.cpp | json_value.cpp | 531 | IndVarLogNeg | otherSize | (!otherSize)
102 | json_value.MUT2715.cpp | json_value.cpp | 544 | DirVarRepExt | other | nullRef
103 | json_value.MUT2735.cpp | json_value.cpp | 547 | DirVarRepExt | other | null
104 | json_value.MUT2780.cpp | json_value.cpp | 553 | VSCR | int_ | bool_
105 | json_value.MUT2799.cpp | json_value.cpp | 555 | DirVarRepExt | other | null
106 | json_value.MUT3052.cpp | json_value.cpp | 576 | ORRN | == | <=
107 | json_value.MUT3147.cpp | json_value.cpp | 597 | SRSR | decodePrefixedString(this->isAllocated() | return nullptr;
108 | json_value.MUT3170.cpp | json_value.cpp | 599 | IndVarIncDec | this_str | (--this_str)
109 | json_value.MUT3370.cpp | json_value.cpp | 644 | ArgLogNeg | this->value_.int_ | !(this->value_.int_)
110 | json_value.MUT3435.cpp | json_value.cpp | 661 | VTWD | this->value_.uint_ | (this->value_.uint_+1)
111 | json_value.MUT3446.cpp | json_value.cpp | 665 | VSCR | real_ | int_
112 | json_value.MUT3643.cpp | json_value.cpp | 714 | IndVarAriNeg | 1 | (-1)
113 | json_value.MUT3782.cpp | json_value.cpp | 767 | ArgBitNeg | this->value_.uint_ | ~(this->value_.uint_)
114 | json_value.MUT3907.cpp | json_value.cpp | 797 | CRCR | this->value_.bool_ | (4294967295)
115 | json_value.MUT3961.cpp | json_value.cpp | 811 | CRCR | this->value_.int_ | (0)
116 | json_value.MUT4036.cpp | json_value.cpp | 817 | ORBN | != | |
117 | json_value.MUT4133.cpp | json_value.cpp | 830 | ORAN | == | /
118 | json_value.MUT4202.cpp | json_value.cpp | 836 | ORLN | == | &&
119 | json_value.MUT4321.cpp | json_value.cpp | 841 | OLLN | \|\| | &&
120 | json_value.MUT4347.cpp | json_value.cpp | 843 | OLLN | \|\| | &&
121 | json_value.MUT4379.cpp | json_value.cpp | 845 | ORRN | == | >
122 | json_value.MUT4402.cpp | json_value.cpp | 847 | OLNG | this->type() == stringValue | !(this->type() == stringValue)
123 | json_value.MUT4413.cpp | json_value.cpp | 848 | ORLN | == | \|\|
124 | json_value.MUT4426.cpp | json_value.cpp | 850 | OLAN | \|\| | -
125 | json_value.MUT4568.cpp | json_value.cpp | 883 | OLNG | this->isNull() | !(this->isNull())
126 | json_value.MUT4610.cpp | json_value.cpp | 888 | FunCalDel | this->isNull() | (0)
127 | json_value.MUT4671.cpp | json_value.cpp | 912 | DirVarLogNeg | newSize | (!newSize)
128 | json_value.MUT4888.cpp | json_value.cpp | 919 | VTWD | index | (index+1)
129 | json_value.MUT4993.cpp | json_value.cpp | 945 | DirVarBitNeg | index | (~index)
130 | json_value.MUT5034.cpp | json_value.cpp | 955 | ArgRepReq | key | (4294967295)
131 | json_value.MUT5046.cpp | json_value.cpp | 957 | RetStaDel | return nullSingleton(); | 
132 | json_value.MUT5084.cpp | json_value.cpp | 965 | IndVarIncDec | index | (--index)
133 | json_value.MUT5240.cpp | json_value.cpp | 991 | FunCalDel | other.isAllocated() | (0)
134 | json_value.MUT5616.cpp | json_value.cpp | 1076 | DirVarIncDec | index | (++index)
135 | json_value.MUT5646.cpp | json_value.cpp | 1077 | IndVarRepExt | defaultValue | nullRef
136 | json_value.MUT5675.cpp | json_value.cpp | 1080 | ORRN | < | >
137 | json_value.MUT5747.cpp | json_value.cpp | 1093 | SRSR | return &(* it).second; | return nullptr;
138 | json_value.MUT5787.cpp | json_value.cpp | 1102 | FunCalDel | this->find(key | 0
139 | json_value.MUT5846.cpp | json_value.cpp | 1108 | ArgRepReq | key.data() + key.length() | 0
140 | json_value.MUT6050.cpp | json_value.cpp | 1138 | IndVarBitNeg | index | (~index)
141 | json_value.MUT6078.cpp | json_value.cpp | 1145 | DirVarIncDec | index | (--index)
142 | json_value.MUT6171.cpp | json_value.cpp | 1148 | IndVarRepPar | i | index
143 | json_value.MUT6190.cpp | json_value.cpp | 1149 | ArgRepReq | i | -1
144 | json_value.MUT6238.cpp | json_value.cpp | 1151 | DirVarIncDec | index | (--index)
145 | json_value.MUT6433.cpp | json_value.cpp | 1164 | DirVarLogNeg | defaultValue | (!defaultValue)
146 | json_value.MUT6542.cpp | json_value.cpp | 1177 | FunCalDel | std::move(it->second) | 1
147 | json_value.MUT6740.cpp | json_value.cpp | 1202 | DirVarRepCon | index | 1
148 | json_value.MUT7027.cpp | json_value.cpp | 1230 | FunCalDel | this->isMember(key.data() | (4294967295)
149 | json_value.MUT7206.cpp | json_value.cpp | 1262 | CRCR | minInt | (2147483647)
150 | json_value.MUT7300.cpp | json_value.cpp | 1274 | SRSR | return false; | return this->value_.int_ >= minInt && this->value_.int_ <= maxInt;
151 | json_value.MUT7387.cpp | json_value.cpp | 1292 | IndVarLogNeg | 0 | (!0)
152 | json_value.MUT7468.cpp | json_value.cpp | 1311 | STRP | return this->value_.real_ >= double(minInt64) && this->value_.real_ < double(maxInt64) && IsIntegral(this->value_.real_); | kill(getpid()
153 | json_value.MUT7491.cpp | json_value.cpp | 1312 | ORRN | < | >
154 | json_value.MUT7617.cpp | json_value.cpp | 1341 | SRSR | switch (this->type()) { | return true;
155 | json_value.MUT7663.cpp | json_value.cpp | 1351 | OLLN | && | \|\|
156 | json_value.MUT7694.cpp | json_value.cpp | 1363 | ORRN | == | >=
157 | json_value.MUT7934.cpp | json_value.cpp | 1405 | FunCalDel | std::move(comment) | 1
158 | json_value.MUT8095.cpp | json_value.cpp | 1431 | DirVarIncDec | limit | (++limit)
159 | json_value.MUT8464.cpp | json_value.cpp | 1532 | ORBN | == | &
160 | json_value.MUT8990.cpp | json_value.cpp | 1578 | OLNG | !node->isValidIndex(arg.index_) | !(!node->isValidIndex(arg.index_))
161 | json_value.MUT9010.cpp | json_value.cpp | 1582 | SRSR | node = &((*node)[arg.index_]) | return Value::nullSingleton();
162 | json_value.MUT9053.cpp | json_value.cpp | 1586 | SRSR | return Value::nullSingleton(); | return *node;

