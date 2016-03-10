# -*- coding: utf-8 -*-

import json
import re
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
from pprint import pprint

parser = DataParser()
csv_parser = CSVParser()

####
# INPUT FOR THE SCRIPT
####
main_data_file = "data/data_all.json"
normal_questions = ["batch1.csv", "batch2.csv", "batch3.csv", "batch4.csv", "batch5.csv",
                    "batch100.csv", "batch101.csv",
                    "batch1sq.csv", "batch2sq.csv", "batch3sq.csv", "batch4sq.csv", "batch5sq.csv",
                    "batch100sq.csv", "batch101sq.csv",]

paraphrased_question = ["batch1-paraphrase.csv", "batch2-paraphrase.csv", "batch3-paraphrase.csv",
                        "batch4-paraphrase.csv", "batch5-paraphrase.csv",
                        "batch100-paraphrase.csv", "batch101-paraphrase.csv",
                        "batch1sq-paraphrase.csv", "batch2sq-paraphrase.csv", "batch3sq-paraphrase.csv",
                        "batch4sq-paraphrase.csv", "batch5sq-paraphrase.csv",
                        "batch100sq-paraphrase.csv", "batch101sq-paraphrase.csv",]

documents_json_file = "bonggun_data/documents.json"
questions_json_file = "bonggun_data/questions.json"

####

with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

# file_to_get_from = "batch1.csv"
# annotated_data = csv_parser.extract_batch_file(segmented_data, file_to_get_from)
#
# #print ("annotated data, [:5]:")
# #pprint(annotated_data[:5])


paragraphs_list = []
doc_dict = {"doc_id": None, "text": ""}

print ("segmented[0]: \nP: %s\nText: %s" % (segmented_data[0]["paragraph_id"], segmented_data[0]["Text"]))
print ("\n\nsegmented[1]: \nP: %s\nText:%s" % (segmented_data[1]["paragraph_id"], segmented_data[1]["Text"]))
#print ("segmented[2]: %s" % segmented_data[2])
exit(1)

for i in segmented_data:
    paragraphs_list.append({"paragraph_id": i["paragraph_id"], "text": i["Text"]})

#print ("docs_list[:5]: ")
#pprint (docs_list[:5])
#print ("name: %s" % i["Name"])

#print docs_list[0]["text"]

with open(documents_json_file, 'w') as fp:
    json.dump(paragraphs_list, fp)

all_questions = []
for i in normal_questions:
    annotated_data = csv_parser.extract_batch_file(segmented_data, i)
    for j in annotated_data:
        question = {"question": j["question"], "paragraph_id": j["paragraph_id"]}
        all_questions.append(question)

for i in paraphrased_question:
    annotated_data = csv_parser.extract_paraphrase_batch_file(segmented_data, i)

    #print ("annotated data [:5]:")
    #pprint(annotated_data[:5])

    for j in annotated_data:
        question = {"question": j["question-paraphrase"], "paragraph_id": j["paragraph_id"]}
        all_questions.append(question)


with open(questions_json_file, 'w') as fp:
   json.dump(all_questions, fp)