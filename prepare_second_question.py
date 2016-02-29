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

file_to_get_from = "batch1.csv"
paraphrase_input_file = "batch1-second-question.csv"

annotated_data = csv_parser.extract_batch_file(segmented_data, file_to_get_from)

csv_parser.prepare_batch_file_for_second_question(annotated_data, paraphrase_input_file)