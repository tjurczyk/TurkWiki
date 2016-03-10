# -*- coding: utf-8 -*-

import json
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
import mturk
from pprint import pprint

parser = DataParser()
csv_parser = CSVParser()

####
# INPUT FOR THE SCRIPT
####

main_data_file = "data/data2.json"
file_to_get_from = "batch101sq.csv"
paraphrase_input_file = "batch101sq-paraphrase.csv"

####

# This is main data (from Tim)
with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

annotated_data = csv_parser.extract_batch_file(segmented_data, file_to_get_from)

csv_parser.prepare_batch_file_for_paraphrase(annotated_data, paraphrase_input_file)