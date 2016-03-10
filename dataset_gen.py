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

####


# This is main data (from Tim)
with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

annotated_paragraphs = []
batch_files = ["batch1.csv", "batch2.csv", "batch3.csv", "batch4.csv", "batch5.csv", "batch100.csv", "batch101.csv",
               "batch1sq.csv", "batch2sq.csv", "batch3sq.csv", "batch4sq.csv", "batch5sq.csv",
               "batch100sq.csv", "batch101sq.csv"]

for i in batch_files:
    annotated_paragraphs.extend(csv_parser.extract_batch_file(segmented_data, i))

print ("Extracted %d paragraphs (questions)" % len(annotated_paragraphs))

# generate tsv file
#print (annotated_paragraphs[0])

data_generator.generate_txt_file(annotated_paragraphs, "test.txt")
dep_data_generator.generate_file(annotated_paragraphs, "data_to_parse.txt")