import json
from data import DataParser, CSVParser, DataGenerator, DEPDataParser
import mturk, pickle
from pprint import pprint
import nltk


parser = DataParser()
csv_parser = CSVParser()

data_generator = DataGenerator()
dep_data_generator = DEPDataParser()

####
# INPUT FOR THE SCRIPT
####

main_data_file = "data/data_all.json"
sample_file = "final_data_work/validate.txt"
fix_file = "fix_turk_result.csv"

####

# This is main data (from Tim)
with open(main_data_file) as data_file:
    data = json.load(data_file)

# Segment it into json
segmented_data = parser.parse_data(data)

fixed_questions = csv_parser.extract_fix_paraphrase_file(fix_file)
print ("Fixed questions has length of %d" % len(fixed_questions))

p_data = csv_parser.parse_all_data(segmented_data, [{"question": ["batch1.csv", "batch2.csv", "batch3.csv",
                                                                  "batch4.csv", "batch5.csv"],
                                                     "paraphrase": ["batch1-paraphrase.csv", "batch2-paraphrase.csv",
                                                                    "batch3-paraphrase.csv", "batch4-paraphrase.csv",
                                                                    "batch5-paraphrase.csv"]},
                                                    {"question": ["batch1sq.csv", "batch2sq.csv", "batch3sq.csv",
                                                                  "batch4sq.csv", "batch5sq.csv"],
                                                     "paraphrase": ["batch1sq-paraphrase.csv", "batch2sq-paraphrase.csv",
                                                                    "batch3sq-paraphrase.csv", "batch4sq-paraphrase.csv",
                                                                    "batch5sq-paraphrase.csv"]},
                                                    {"question": ["batch100.csv", "batch101.csv"],
                                                     "paraphrase": ["batch100-paraphrase.csv",
                                                                    "batch101-paraphrase.csv"]},
                                                    {"question": ["batch100sq.csv", "batch101sq.csv"],
                                                     "paraphrase": ["batch100sq-paraphrase.csv",
                                                                    "batch101sq-paraphrase.csv"]}], fixed_questions)

def get_entity_for_question(q_text):
    candidate = None
    for k, v in p_data.iteritems():
        for l in v:
            if candidate and l["question"] == q_text:
                print ("Found duplicated question entity!")
                exit(1)
            if l["question"] == q_text.decode('Unicode'):
                # print ("Found in paragraph: %s" % l["paragraph_id"])
                candidate = l
            if "Who donated a broad range of material to the Metropolitan Museum of Art in" in l["question"]:
                print ("Comparing question: %s\nTo question: %s" % (q_text, l["question"]))

    print ("Returning none for question: %s" % q_text)
    return candidate


# Read sample file
f = open(sample_file, "r")
question = None
questions = 0

for line in f:
    q, s, label = line.split("\t")
    if question == None or question != q:
        questions += 1
        question = q
        q_entity = get_entity_for_question(question)
        # print ("Working on question: %s" % question)
        # print ("Got entity question: %s" % q_entity["question"])


# print ("In file %s I counted %d questions" % (sample_file, questions))