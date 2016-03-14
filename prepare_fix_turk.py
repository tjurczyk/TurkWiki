# -*- coding: utf-8 -*-

import json
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
import mturk
from pprint import pprint


parser = DataParser()
csv_parser = CSVParser()

data_generator = DataGenerator()
dep_data_generator = DEPDataParser()


def get_data_for_question(packed_data, question, paragraph):
    for k, v in packed_data.iteritems():
        for j in v:
            if j["paragraph_id"] == paragraph and j["question"] == question:
                return True, j

    return False, None


####
# INPUT FOR THE SCRIPT
####

main_data_file = "data/data_all.json"
file_from_bonggun = "error.json"

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

with open(file_from_bonggun) as data_file:
    data_from_bonggun = json.load(data_file)

# for i in data_from_bonggun:
#     print ("q: %s" % i["question"])

print ("len of bonggun data: %d" % len(data_from_bonggun))

dic = {True: 0, False: 0}
selected_data = []

for i in data_from_bonggun:
    val, item = get_data_for_question(p_data, i["question"], i["paragraph_id"])
    dic[val] += 1
    selected_data.append(item)
    candidates = item["candidates"].split(",")
    # if len(candidates) == 1:
    #print ("Question from Bonggun: %s\nFile: %s\n" % (i["question"], item["filename"]))
    # else:
    #     continue

csv_parser.prepare_batch_file_for_fixing_question(selected_data, "fix_turk.csv")

pprint (dic)