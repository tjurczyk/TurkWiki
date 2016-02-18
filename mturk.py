# -*- coding: utf-8 -*-

import json
from data import DataParser, CSVParser, AnnotationAnalyzer


parser = DataParser()
csv_parser = CSVParser()


def extract_all_annotated_paragraphs(seg_data, file_names):
    annotated_paragraphs = set()

    for i in file_names:
        # get all paragraphs from this batch file
        output = csv_parser.extract_batch_file(seg_data, i)

        for j in output:
            if j["paragraph_id"] in annotated_paragraphs:
                print ("Found paragraph id that is duplicated! '%s'" % j["paragraph_id"])

            annotated_paragraphs.add(j["paragraph_id"])

    return annotated_paragraphs


def generate_batch_input(segmented_data, batch_file_name, already_annotated_file_names=None):
    already_annotated = None
    if already_annotated_file_names:
        already_annotated = extract_all_annotated_paragraphs(segmented_data, already_annotated_file_names)

    new_data = parser.select_data(segmented_data, already_annotated)
    csv_parser.prepare_batch_file(new_data, batch_file_name)


def analyze_batch_results(segmented_data, filename):
    output = csv_parser.extract_batch_file(segmented_data, filename)

    aa = AnnotationAnalyzer()
    aa.analyze_results(output)


if __name__ == "__main__":
    pass
    # This is main data (from Tim)
    #with open('data.json') as data_file:
    #    data = json.load(data_file)

    # Segment it into json
    #segmented_data = parser.parse_data(data)

    # Creating batch input
    #batch_fname = "wiki-5.csv"
    #already_annotated_files = ["batch1.csv", "batch2.csv", "batch3.csv", "batch4.csv"]
    #generate_batch_input(segmented_data, batch_fname, already_annotated_files)

    # Analyzing batch results (csv from MTurk)
    #filename = "batch5.csv"
    #analyze_batch_results(segmented_data, filename)