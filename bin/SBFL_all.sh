# ./build.py --project jsoncpp --bug_version bug1 --withPreprocessed
# ./gen_data.py --project jsoncpp --bug_version bug1 --criteria_per_BUG
# ./gen_data.py --project jsoncpp --bug_version bug1 --spectra_data
# ./gen_data.py --project jsoncpp --bug_version bug1 --processed_data
# ./gen_data.py --project jsoncpp --bug_version bug1 --ranked_data
./SBFL_bug1.sh

# ./build.py --project jsoncpp --bug_version bug2 --withPreprocessed
# ./gen_data.py --project jsoncpp --bug_version bug2 --criteria_per_BUG
# ./gen_data.py --project jsoncpp --bug_version bug2 --spectra_data
# ./gen_data.py --project jsoncpp --bug_version bug2 --processed_data
# ./gen_data.py --project jsoncpp --bug_version bug2 --ranked_data
./SBFL_bug2.sh

# ./build.py --project jsoncpp --bug_version bug3 --withPreprocessed
# ./gen_data.py --project jsoncpp --bug_version bug3 --criteria_per_BUG
# ./gen_data.py --project jsoncpp --bug_version bug3 --spectra_data
# ./gen_data.py --project jsoncpp --bug_version bug3 --processed_data
# ./gen_data.py --project jsoncpp --bug_version bug3 --ranked_data
./SBFL_bug3.sh
 
# ./build.py --project jsoncpp --bug_version bug4 --withPreprocessed
# ./gen_data.py --project jsoncpp --bug_version bug4 --criteria_per_BUG
# ./gen_data.py --project jsoncpp --bug_version bug4 --spectra_data
# ./gen_data.py --project jsoncpp --bug_version bug4 --processed_data
# ./gen_data.py --project jsoncpp --bug_version bug4 --ranked_data
./SBFL_bug4.sh

./gather.py
