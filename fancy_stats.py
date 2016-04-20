# -*- coding: utf-8 -*-

import json
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
import mturk
import nltk
from pprint import pprint


parser = DataParser()
csv_parser = CSVParser()

data_generator = DataGenerator()
dep_data_generator = DEPDataParser()

####
# INPUT FOR THE SCRIPT
####

main_data_file = "data/data_all.json"

####


# This is main data (from Tim)
with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

# pprint(segmented_data[:4])

# wt = nltk.RegexpTokenizer(r'\w+').tokenize
# words_count = 0
#
# for p in segmented_data:
#     for s in p["sentences"]:
#         words_count += len(wt(s))
#
# print ("Words count: %d" % words_count)
#
#
# g = {}
#
# d = segmented_data[0]["Name"]
# g[segmented_data[0]["Type"]] = 1
#
# for i in segmented_data:
#     if i["Name"] != d:
#         if i["Type"] not in g:
#             g[i["Type"]] = 1
#         else:
#             g[i["Type"]] += 1
#         d = i["Name"]
#
# g[segmented_data[len(segmented_data)-1]["Type"]] += 1
#
# pprint(g)


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

fix_file = "fix_turk_result.csv"
fixed_questions = csv_parser.extract_fix_paraphrase_file(fix_file)

# print("keys: %s" % p_data.keys())
# print ("Fixed questions: ")
# pprint(fixed_questions[:20])

import pickle
f = open("bonggun_data/all_questions.pickle", "wb")
pickle.dump(p_data, f)
f.close()

f = open("bonggun_data/paraphrases.pickle", "wb")
pickle.dump(fixed_questions, f)
f.close()