# -*- coding: utf-8 -*-

import json
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
import mturk, pickle
from pprint import pprint
import nltk


parser = DataParser()
csv_parser = CSVParser()

data_generator = DataGenerator()
dep_data_generator = DEPDataParser()

####
# INPUT FOR THE SCRIPT
####

main_data_file = "data/data_all.json"
split_values = {"train": 0.7, "validate": 0.1, "test": 0.2}
fix_file = "fix_turk_result.csv"

####

# This is main data (from Tim)
with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)


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
                                                                    "batch101sq-paraphrase.csv"]}])
#
#
# single = 0
# multi = 0
#
# for i, j in p_data.iteritems():
#     for k in j:
#         # print ("i: %s" % i)
#         if len(k["candidates"].split(",")) > 1:
#             multi += 1
#         else:
#             single += 1
#
# print ("Single: %d, multi: %d" % (single, multi))

fix_file = "fix_turk_result.csv"
fixed_questions = csv_parser.extract_fix_paraphrase_file(fix_file)


def check_fix_data(l, p_id, q):
    for x in l:
        if x["question"] == q and x["paragraph_id"] == p_id:
            return True
    return False

single = 0
multi = 0

print ("len of fixed: %d" % len(fixed_questions))

for i, j in p_data.iteritems():
    for k in j:
        check_fix_data(fixed_questions, k["paragraph_id"], k["question"])
        if check_fix_data(fixed_questions, k["paragraph_id"], k["question"]) == True:
            if len(k["candidates"].split(",")) > 1:
                multi += 1
            else:
                single += 1

print ("Single: %d, multi: %d" % (single, multi))