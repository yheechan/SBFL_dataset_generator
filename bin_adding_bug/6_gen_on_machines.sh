date
ssh faster2 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
sleep 1s
ssh faster4 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster5 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster7 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster8 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster9 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
sleep 1s
ssh faster14 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster15 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster16 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster17 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster18 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
sleep 1s
ssh faster19 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster20 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster21 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster23 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster24 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
sleep 1s
ssh faster25 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster26 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster27 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
ssh faster29 "cd SBFL_dataset_generator/bin_run_on_machine && ./command.py > output.0 2>&1" & 
echo ssh done, waiting...
date
wait
date
