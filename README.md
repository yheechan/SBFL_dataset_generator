# gen_data_4_jsoncpp

## ToDo
* analyze all test cases given in JsonCPP
* generate a more detailed data for JsonCPP
TC that:
  1. NOT executes buggy **lines**
  2. executes buggy **lines**
  3. Not executes **cpp file** containing buggy line
  4. executes **cpp file** containing buggy line
  5. Not executes **class** containing buggy line
  6. executes **class** containing buggy line
  7. Not executes **function** containing buggy line
  8. executes **function** containing buggy line
* analyze ossfuzz timeout bugs
* implement tool for calculating difference between test cases
  * intersections of ```<# of lines, # of functions, # of files>```

