# -*- coding: utf-8 -*-

import json
import pickle
import re
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
from pprint import pprint

parser = DataParser()
csv_parser = CSVParser()

####
# INPUT FOR THE SCRIPT
####
main_data_file = "data/data_all.json"
fix_file = "fix_turk_result.csv"

######

with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

d = {}

for i in segmented_data:
    d[i["paragraph_id"]] = i["Type"]

f = open("pid_to_type", "wb")
pickle.dump(d, f)