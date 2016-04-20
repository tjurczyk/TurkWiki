# -*- coding: utf-8 -*-

import json
import pickle
import re
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
from pprint import pprint

parser = DataParser()
csv_parser = CSVParser()

####
# INPUT FOR THE SCRIPT
####
main_data_file = "data/data_all.json"
fix_file = "fix_turk_result.csv"

######

with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

# d = {}
#
# for i in segmented_data:
#     d[i["paragraph_id"]] = i["Type"]
#
# f = open("pid_to_type", "wb")
# pickle.dump(d, f)

fixed_questions = csv_parser.extract_fix_paraphrase_file(fix_file)
print ("Fixed questions has length of %d" % len(fixed_questions))


p_data = csv_parser.parse_all_data(segmented_data, [{"question": ["batch1.csv", "batch2.csv", "batch3.csv",
                                                                  "batch4.csv", "batch5.csv"],
                                                     "paraphrase": ["batch1-paraphrase.csv", "batch2-paraphrase.csv",
                                                                    "batch3-paraphrase.csv", "batch4-paraphrase.csv",
                                                                    "batch5-paraphrase.csv"]},
                                                    {"question": ["batch1sq.csv", "batch2sq.csv", "batch3sq.csv",
                                                                  "batch4sq.csv", "batch5sq.csv"],
                                                     "paraphrase": ["batch1sq-paraphrase.csv", "batch2sq-paraphrase.csv",
                                                                    "batch3sq-paraphrase.csv", "batch4sq-paraphrase.csv",
                                                                    "batch5sq-paraphrase.csv"]},
                                                    {"question": ["batch100.csv", "batch101.csv"],
                                                     "paraphrase": ["batch100-paraphrase.csv",
                                                                    "batch101-paraphrase.csv"]},
                                                    {"question": ["batch100sq.csv", "batch101sq.csv"],
                                                     "paraphrase": ["batch100sq-paraphrase.csv",
                                                                    "batch101sq-paraphrase.csv"]}], fixed_questions)


b_dict = {}

# pprint(p_data["ART"][:2])

for k, v in p_data.iteritems():
    for j in v:
        if j["question"] in b_dict:
            print("Duplicate question!")

        b_dict[j["question"]] = j["is_paraphrase"]

# f = open("question_to_p_notp.pickle", "wb")
# pickle.dump(b_dict, f)

f = open("analysis_ss/test_list_for_analysis.pickle", "rb")
test_s = pickle.load(f)
f.close()

for i in test_s:
    i["is_paraphrased"] = b_dict[i["question"]]

f = open("analysis_ss/test_list_for_analysis.pickle", "wb")
pickle.dump(test_s, f)