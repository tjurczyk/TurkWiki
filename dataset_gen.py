# -*- coding: utf-8 -*-

import json
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
import mturk
from pprint import pprint


parser = DataParser()
csv_parser = CSVParser()

# This is main data (from Tim)
with open('data.json') as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

annotated_paragraphs = []
batch_files = ["batch1.csv", "batch2.csv", "batch3.csv", "batch4.csv", "batch5.csv"]

for i in batch_files:
    annotated_paragraphs.extend(csv_parser.extract_batch_file(segmented_data, i))

# generate tsv file
#print (annotated_paragraphs[0])

data_gen = DataGenerator()
data_gen.generate_txt_file(annotated_paragraphs, "test.txt")

#dep_data_gen = DEPDataParser()

#dep_data_gen.generate_file(annotated_paragraphs, "data_to_parse.txt")