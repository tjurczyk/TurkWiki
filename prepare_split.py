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

categories = {}
docs = {}
paragraphs = 0

for i in segmented_data:
    paragraphs += 1
    if i["Name"] not in docs:
        docs[i["Name"]] = True
        if i["Type"] not in categories:
            categories[i["Type"]] = 1
        else:
            print ("Will be incrementing %s")
            categories[i["Type"]] += 1


pprint(categories)
print ("%d paragraphs" % paragraphs)