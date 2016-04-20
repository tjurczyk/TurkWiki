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
filename_to_analyze_from = "batch101sq.csv"

####

# This is main data (from Tim)`
with open(main_data_file) as data_file:
    data = json.load(data_file)

segmented_data = parser.parse_data(data)

# Analyzing batch results (csv from MTurk)
annotated_data = csv_parser.extract_batch_file(segmented_data, filename_to_analyze_from)
aa.analyze_results(annotated_data)