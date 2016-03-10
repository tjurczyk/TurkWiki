# -*- coding: utf-8 -*-

import json
from data import DataParser, CSVParser, AnnotationAnalyzer


parser = DataParser()
csv_parser = CSVParser()
aa = AnnotationAnalyzer()

####
# INPUT FOR THE SCRIPT
####

main_data_file = "data/data2.json"
batch_filename = "wiki-101.csv"
already_annotated_files = ['batch100.csv']

####

# This is main data (from Tim)
with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)
# name = None
# docs = 0
#
# for i in segmented_data:
#     #print ("name name: %s" % i["Name"])
#     if name is None or i["Name"] != name:
#         name = i["Name"]
#         docs += 1
#         print ("name: %s" % name)
# print ("There is %d documents." % docs)
already_annotated_paragraphs = set()
for i in already_annotated_files:
    # get all paragraphs from this batch file
    output = csv_parser.extract_batch_file(segmented_data, i)

    for j in output:
        if j["paragraph_id"] in already_annotated_paragraphs:
            print ("Found paragraph id that is duplicated! '%s'" % j["paragraph_id"])

        already_annotated_paragraphs.add(j["paragraph_id"])

new_data = parser.select_data(segmented_data, already_annotated_paragraphs)

# Get all already annotated paragraphs

for i in new_data:
    if i["paragraph_id"] in already_annotated_paragraphs:
        print ("Found paragraph id that is duplicated! '%s'" % i["paragraph_id"])

    already_annotated_paragraphs.add(i["paragraph_id"])

new_data.extend(parser.select_data(segmented_data, already_annotated_paragraphs))
csv_parser.prepare_batch_file(new_data, batch_filename)