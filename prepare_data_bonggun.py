# -*- coding: utf-8 -*-

import json
import re
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
import mturk
from pprint import pprint

parser = DataParser()
csv_parser = CSVParser()

normal_questions = ["batch1.csv", "batch2.csv", "batch3.csv", "batch4.csv", "batch5.csv"]

paraphrased_question = ["batch1-paraphrase.csv", "batch2-paraphrase.csv", "batch3-paraphrase.csv",
                        "batch4-paraphrase.csv", "batch5-paraphrase.csv"]

documents_json_file = "bonggun_data/documents.json"
questions_json_file = "bonggun_data/questions.json"

with open('data.json') as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

# file_to_get_from = "batch1.csv"
# annotated_data = csv_parser.extract_batch_file(segmented_data, file_to_get_from)
#
# #print ("annotated data, [:5]:")
# #pprint(annotated_data[:5])


docs_list = []
doc_dict = {"doc_id": None, "text": ""}

for i in segmented_data:
    if not doc_dict["doc_id"]:
        doc_dict["doc_id"] = i["Name"]
        doc_dict["text"] += re.sub(r'^('+i["Name"]+'|'+i["Section"]+'\.?)', '', i["Text"]) + "\n\n"
    elif doc_dict["doc_id"] != i["Name"]:
        docs_list.append(doc_dict)
        doc_dict = {"doc_id": i["Name"], "text": re.sub(r'^('+i["Name"]+'|'+i["Section"]+'\.?)', '', i["Text"]) + "\n\n"}
    else:
        doc_dict["text"] += re.sub(r'^('+i["Name"]+'|'+i["Section"]+'\.?)', '', i["Text"]) + "\n\n"

docs_list.append(doc_dict)
#print ("docs_list[:5]: ")
#pprint (docs_list[:5])
#print ("name: %s" % i["Name"])

#print docs_list[0]["text"]

with open(documents_json_file, 'w') as fp:
    json.dump(docs_list, fp)

all_questions = []
for i in normal_questions:
    annotated_data = csv_parser.extract_batch_file(segmented_data, i)
    for j in annotated_data:
        question = {"question": j["question"], "doc_id": j["name"]}
        all_questions.append(question)

for i in paraphrased_question:
    annotated_data = csv_parser.extract_paraphrase_batch_file(segmented_data, i)

    #print ("annotated data [:5]:")
    #pprint(annotated_data[:5])

    for j in annotated_data:
        question = {"question": j["question-paraphrase"], "doc_id": j["name"]}
        all_questions.append(question)


with open(questions_json_file, 'w') as fp:
   json.dump(all_questions, fp)