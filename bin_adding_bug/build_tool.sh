mkdir build
cd build
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_FLAGS="-O0 -fprofile-arcs -ftest-coverage -g -fno-omit-frame-pointer -gline-tables-only -DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION -fsanitize=address,undefined -fsanitize-address-use-after-scope" \
  -DBUILD_SHARED_LIBS=OFF -G "Unix Makefiles" ../
make -j20
clang++ -O0 \
  -fprofile-arcs -ftest-coverage -g \
  -fno-omit-frame-pointer -gline-tables-only \
  -DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION \
  -fsanitize=address,undefined \
  -fsanitize-address-use-after-scope \
  -fsanitize=fuzzer \
  -I../include \
  -disabled-shared \
  ../src/test_lib_json/fuzz.cpp -o jsoncpp_fuzzer \
  ./src/lib_json/libjsoncpp.a
