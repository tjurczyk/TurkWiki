# -*- coding: utf-8 -*-

import json
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
import mturk
from pprint import pprint


parser = DataParser()
csv_parser = CSVParser()

data_generator = DataGenerator()
dep_data_generator = DEPDataParser()

####
# INPUT FOR THE SCRIPT
####

main_data_file = "data/data_all.json"
split_values = {"train": 0.7, "validate": 0.1, "test": 0.2}

####

# This is main data (from Tim)
with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

# categories = {}
# docs = {}
# paragraphs = 0
#
# for i in segmented_data:
#     paragraphs += 1
#     if i["Name"] not in docs:
#         docs[i["Name"]] = True
#         if i["Type"] not in categories:
#             categories[i["Type"]] = 1
#         else:
#             print ("Will be incrementing %s")
#             categories[i["Type"]] += 1
#
#
# pprint(categories)
# print ("%d paragraphs" % paragraphs)

#p_data = csv_parser.extract_paraphrase_batch_file(segmented_data, "batch1-paraphrase.csv")
# p_data = csv_parser.extract_batch_file(segmented_data, "batch1.csv")

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

print ("\nParsed all data:")
for k, v in p_data.iteritems():
    print ("Key %s has %d paragraphs" % (k, len(v)))

print("\n")
data_splits = data_generator.prepare_split_paragraphs(split_values, p_data)

for i in ["train", "validate", "test"]:
    file_name = i + ".txt"
    dep_file_name = i + "_to_parse.txt"
    print ("Packing %s set with the size of %d samples to file: %s and dep data to file %s" %
           (i, len(data_splits[i]), file_name, dep_file_name))
    data_generator.generate_txt_file(data_splits[i], i + ".txt")
    dep_data_generator.generate_file(data_splits[i], i + "_to_parse.txt")


# pprint(p_data)
# print ("Length of returned data: %d" % len(p_data))