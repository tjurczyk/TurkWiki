# -*- coding: utf-8 -*-

import json
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
import mturk, pickle
from pprint import pprint
import nltk
from random import shuffle


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

fixed_questions = csv_parser.extract_fix_paraphrase_file(fix_file)
print ("Fixed questions has length of %d" % len(fixed_questions))

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

############
# ALL DATA


############

############
# Only Q + SQ

# p_data = csv_parser.parse_all_data(segmented_data, [#{"question": ["batch1.csv", "batch2.csv", "batch3.csv",
#                                                     #              "batch4.csv", "batch5.csv"],
#                                                     # "paraphrase": []},
#                                                     {"question": ["batch1sq.csv", "batch2sq.csv", "batch3sq.csv",
#                                                                   "batch4sq.csv", "batch5sq.csv"],
#                                                      "paraphrase": []},
#                                                     #{"question": ["batch100.csv", "batch101.csv"],
#                                                     # "paraphrase": []},])
#                                                     {"question": ["batch100sq.csv", "batch101sq.csv"],
#                                                      "paraphrase": []}])

############


############
# Only PQ + PSQ


# p_data = csv_parser.parse_paraphrase_data(segmented_data, [{"question": ["batch1.csv", "batch2.csv", "batch3.csv",
#                                                                   "batch4.csv", "batch5.csv"],
#                                                      "paraphrase": ["batch1-paraphrase.csv", "batch2-paraphrase.csv",
#                                                                     "batch3-paraphrase.csv", "batch4-paraphrase.csv",
#                                                                     "batch5-paraphrase.csv"]},
#                                                     {"question": ["batch1sq.csv", "batch2sq.csv", "batch3sq.csv",
#                                                                   "batch4sq.csv", "batch5sq.csv"],
#                                                      "paraphrase": ["batch1sq-paraphrase.csv", "batch2sq-paraphrase.csv",
#                                                                     "batch3sq-paraphrase.csv", "batch4sq-paraphrase.csv",
#                                                                     "batch5sq-paraphrase.csv"]},
#                                                     {"question": ["batch100.csv", "batch101.csv"],
#                                                      "paraphrase": ["batch100-paraphrase.csv",
#                                                                     "batch101-paraphrase.csv"]},
#                                                     {"question": ["batch100sq.csv", "batch101sq.csv"],
#                                                      "paraphrase": ["batch100sq-paraphrase.csv",
#                                                                     "batch101sq-paraphrase.csv"]}])


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


############


print ("\nParsed all data:")
for k, v in p_data.iteritems():
    print ("Key %s has %d paragraphs" % (k, len(v)))

print("\n")
data_splits = data_generator.prepare_split_paragraphs(split_values, p_data)

# Here, we do a file for later analysis from ConvNet
# It contains:
#  - genera (MUSIC/TV...)
#  - q_len
#  - s_len (number of sentences in a paragraph)
#  - q_type (wh* + how + other)


wt = nltk.RegexpTokenizer(r'\w+').tokenize
q_types_words = set(["what", "why", "when", "who", "where", "how"])

for spl in ["train", "validate", "test"]:
    list_for_analysis = []
    shuffle(data_splits[spl])

    for i in data_splits[spl]:
        #print ("i: ")
        #pprint(i)
        in_dict = {'question': i["question"], 'genera': i["type"]}

        q_words = [x.lower() for x in wt(i["question"])]
        in_dict['q_len'] = len(q_words)
        in_dict['s_len'] = len(i["sentences"])

        q_types = set()
        for w in q_words:
            if w in q_types_words:
                q_types.add(w)

        if len(q_types):
            in_dict["q_types"] = list(q_types)

        in_dict["q_is_paraphrase"] = i["is_paraphrase"]

        list_for_analysis.append(in_dict)

    # Store dict for analysis
    print ("Created the list of " + spl + " for analysis with the length of %d" % len(list_for_analysis))
    f_pickle = open("gen_data/" + spl + "_list_for_analysis.pickle", "wb")
    pickle.dump(list_for_analysis, f_pickle, protocol=2)
    f_pickle.close()

    print ("Created the list of " + spl + " of raw data with the length of %d" % len(data_splits[spl]))
    # Store raw dict (all paragraphs ordered)
    f_pickle = open("gen_data/" + spl + "_raw_list.pickle", "wb")
    pickle.dump(data_splits[spl], f_pickle, protocol=2)
    f_pickle.close()

print ("\n")

for i in ["train", "validate", "test"]:
    file_name = i + ".txt"
    dep_file_name = i + "_to_parse.txt"
    print ("Packing %s set with the size of %d samples to file: %s and dep data to file %s" %
           (i, len(data_splits[i]), file_name, dep_file_name))
    data_generator.generate_txt_file(data_splits[i], i + ".txt")
    dep_data_generator.generate_file(data_splits[i], i + "_to_parse.txt")


# pprint(p_data)
# print ("Length of returned data: %d" % len(p_data))