# gen_data_4_jsoncpp

## ToDo
* analyze all test cases given in JsonCPP
* generate a more detailed data for JsonCPP
TC that:
  1. Not executes **cpp file** containing buggy line
  2. executes **cpp file** containing buggy line
  3. Not executes **class** containing buggy line
  4. executes **class** containing buggy line
  5. Not executes **function** containing buggy line
  6. executes **function** containing buggy line
  7. NOT executes buggy **lines**
  8. executes buggy **lines**
* analyze ossfuzz timeout bugs
* implement tool for calculating difference between test cases
  * intersections of ```<# of lines, # of functions, # of files>```

