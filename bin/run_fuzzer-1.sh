UBSAN_OPTIONS=print_stacktrace=1 ./jsoncpp_fuzzer -rss_limit_mb=2560 -timeout=25 -runs=100 tc-heapoverflow -dict=fuzz.dict

