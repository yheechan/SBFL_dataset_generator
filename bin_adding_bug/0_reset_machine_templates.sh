date
ssh faster2 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster2 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster2.0 2>&1" & 
sleep 8s
wait
ssh faster4 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster4 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster4.0 2>&1" & 
ssh faster5 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster5 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster5.0 2>&1" & 
ssh faster7 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster7 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster7.0 2>&1" & 
sleep 8s
wait
ssh faster8 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster8 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster8.0 2>&1" & 
ssh faster9 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster9 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster9.0 2>&1" & 
ssh faster14 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster14 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster14.0 2>&1" & 
sleep 8s
wait
ssh faster15 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster15 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster15.0 2>&1" & 
ssh faster16 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster16 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster16.0 2>&1" & 
ssh faster17 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster17 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster17.0 2>&1" & 
sleep 8s
wait
ssh faster18 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster18 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster18.0 2>&1" & 
ssh faster19 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster19 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster19.0 2>&1" & 
ssh faster20 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster20 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster20.0 2>&1" & 
sleep 8s
wait
ssh faster21 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster21 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster21.0 2>&1" & 
ssh faster23 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster23 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster23.0 2>&1" & 
ssh faster24 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster24 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster24.0 2>&1" & 
sleep 8s
wait
ssh faster25 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster25 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster25.0 2>&1" & 
ssh faster26 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster26 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster26.0 2>&1" & 
ssh faster27 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster27 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster27.0 2>&1" & 
sleep 8s
wait
ssh faster29 "cd SBFL_dataset_generator && rm -rf subjects" 
sleep 1s
wait
ssh faster29 "cd SBFL_dataset_generator/bin_adding_bug && python3 1_make_template.py > output.reset.faster29.0 2>&1" & 
echo ssh done, waiting...
date
wait
date
