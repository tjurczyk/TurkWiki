# -*- coding: utf-8 -*-

import nltk
import re
from pprint import pprint
import csv
import random
from collections import defaultdict
from numpy import mean, median, std

ARTICLE_TYPES = {'MUSIC', 'TV', 'TRAVEL', 'ART', 'SPORT', 'COUNTRY', 'MOVIES', 'HISTORICAL EVENTS', 'SCIENCE', 'FOOD'}


class DataParser:
    MIN_SENTENCES_COUNT = 5
    MAX_SENTENCES_COUNT = 24

    ACCEPTED_ARTICLE_TYPES = None
    SKIPPED_SECTIONS = {'See also', 'See Also', 'References', 'Bibliography', 'Further reading',
                        'External links', 'Footnotes', 'References and sources', 'Sources', 'Visual summary',
                        'Notes'}

    LI_MARKS = {'</li><li>', '<li>', '</li>'}

    tokenizer = None

    def __init__(self):
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def parse_data(self, json):
        d = []

        for i in json:
            item_d = i.copy()
            item_d["sentences"] = []
            item_category = i["Type"]
            item_name = i["Name"]
            item_section = i["Section"]

            if self.ACCEPTED_ARTICLE_TYPES and i["Type"] not in self.ACCEPTED_ARTICLE_TYPES:
                continue

            sentences = self.tokenizer.tokenize(i["Text"])

            if i["Section"] in self.SKIPPED_SECTIONS:
                continue

            # The id for each paragraph is [name]-[section] (spaces to underscores if appear)
            item_d["paragraph_id"] = re.sub(r' ', '_', i["Name"]) + "-" + re.sub(r' ', '_', i["Section"])

            s_id = 1

            sent_str = "Category: " + item_category.title() + "<br/>Title: " + item_name + "<br/>Section: " + item_section + "<br/><br/>"

            for i, s in enumerate(sentences):
                if i == 0:
                    # There most likely is name or section string at the beginning of the sentence
                    s = re.sub(r'^('+item_name+'|'+item_section+'\.?)', '', s)

                split_by_li = re.split(r'(</li><li>|<li>|</li>)', s)
                if len(split_by_li) > 1:
                    for i, ss in enumerate(split_by_li):
                        if ss not in self.LI_MARKS and ss != "":
                            if i != 0:
                                if split_by_li[i-1] == "</li><li>":
                                    #print("Inside if for ss: %s" % ss)
                                    sent_str += str(s_id) + u". •&nbsp;&nbsp;&nbsp;&nbsp;" + ss + "<br/>"
                                elif split_by_li[i-1] == "</li>":
                                    if s_id > 1:
                                        #print("Additionally s_id > 1")
                                        sent_str += "<br/>"
                                    sent_str += str(s_id) + ". " + ss + "</br>"
                                    #print("Inside elif for ss: %s" % ss)
                                elif split_by_li[i-1] == "<li>":
                                    sent_str += str(s_id) + u". •&nbsp;&nbsp;&nbsp;&nbsp;" + ss + "<br/>"
                                    #print("Inside else, ss: %s" % ss)
                            else:
                                sent_str += str(s_id) + ". " + ss + "<br/>"

                            s_id += 1
                            item_d["sentences"].append(ss)

                else:
                    item_d["sentences"].append(s)
                    sent_str += str(s_id) + ". " + s + "<br/>"
                    s_id += 1

            #print("Here, d_item: %s" % (pprint(item_d)))
            item_d["sentences_count"] = len(item_d["sentences"])
            item_d["mt_str"] = sent_str
            d.append(item_d)

        return d

    def select_data(self, json_data, already_annotated=None):
        # Create set of all Article names
        article_names = set()
        [article_names.add(x["Name"]) for x in json_data]

        print ("Inside, size is: %d" % len(article_names))

        already_chosen = set()
        chosen_paragraphs = []
        iteration = 0

        while True:
            i = random.choice(json_data)

            #if iteration % 10000 == 0:
            #    print ("for iteration: %d, len(chosen_paragraphs): %d" % (iteration, len(chosen_paragraphs)))
            iteration += 1

            if iteration >= 10000000:
                break

            #print ("Randomized: %s with sen length: %s" % (i["paragraph_id"], i["sentences_count"]))

            if already_annotated and i["paragraph_id"] in already_annotated:
                continue

            if i["sentences_count"] > self.MAX_SENTENCES_COUNT or i["sentences_count"] < self.MIN_SENTENCES_COUNT:
                continue

            if i["Name"] not in already_chosen:
                chosen_paragraphs.append(i)
                already_chosen.add(i["Name"])

            if len(already_chosen) == len(article_names):
                break

        return chosen_paragraphs


class CSVParser:
    results_batch_dir = "batch-results/"
    input_batch_dir = "batch-input/"

    def __init__(self):
        pass

    def prepare_batch_file(self, json_data, filename):
        writer = csv.writer(open(self.input_batch_dir + filename, "w"))
        writer.writerow(('paragraph_id', 'content'))
        for i in json_data:
            try:
                writer.writerow((i["paragraph_id"].encode("utf-8"), i["mt_str"].encode("utf-8")))
            except KeyError:
                return KeyError("paragraph_id/mt_str not in the dictionary")

    def extract_batch_file(self, json_data, csv_filename):
        csv_data = self.parse_csv_results_file(csv_filename)
        print ("csv_data: %s" % len(csv_data))

        extracted = []
        tmp_added = set()

        #print ("json data: %s" % json_data)

        for i in json_data:
            # print ("Working on paragraph id: %s" % i["paragraph_id"])

            if i["paragraph_id"] in csv_data.keys():
                di = {'paragraph_id': i["paragraph_id"], 'question': csv_data[i["paragraph_id"]]["question"],
                      'candidates': csv_data[i["paragraph_id"]]["candidates"], 'sentences': i["sentences"],
                      'filename': csv_filename}
                extracted.append(di)

        for i in extracted:
            if i["paragraph_id"] in tmp_added:
                print("\n\nHAVE DUPLICATE: %s\n\n" % i["paragraph_id"])

            tmp_added.add(i["paragraph_id"])

        return extracted

    def parse_csv_results_file(self, csv_filename):
        csv_file = open(self.results_batch_dir + csv_filename)
        csv_data = csv.reader(csv_file)

        d = {}

        # print ("csv_data[0]: %s" % type(csv_data))

        q_index = None
        c_index = None
        p_index = None

        for i, row in enumerate(csv_data):
            if i == 0:
                q_index = row.index('Answer.QuestionTextBox')
                c_index = row.index('Answer.QuestionSentencesBox')
                p_index = row.index('Input.paragraph_id')
                continue

            d[unicode(row[p_index], "utf-8")] = {'question': unicode(row[q_index], "utf-8"),
                                                 'candidates': unicode(row[c_index], "utf-8")}

        return d


class AnnotationAnalyzer:
    def __init__(self):
        pass

    def analyze_results(self, data):
        self.print_summary(data)

    def print_summary(self, data):
        #print ("Got data with len of: %d" % len(data))

        print ("Statistics of this csv results file:")
        print (u'\u2022' + " All questions: %d\n" % len(data))

        # Find out distribution of the sentences len
        s_lens = defaultdict(int)
        s_lens_list = []
        for i in data:
            s_lens_list.append(len(i["sentences"]))
            s_lens[len(i["sentences"])] += 1

        print (u'\u2022' + " Distribution of sentence lengths of paragraphs:")
        for k, v in s_lens.iteritems():
            print ("%s: %s (%.2f%%)" % (str(k).rjust(2), v, float(v)/len(data)*100))
        print ("median: %.4f, mean: %.4f, st.dev: %.4f\n" % (median(s_lens_list), mean(s_lens_list), std(s_lens_list)))

        # Find out how many questions are single and multi sentences
        single_multi = {"single": 0, "multi": 0}

        for i in data:
            if len(i["candidates"].split(",")) > 1:
                single_multi["multi"] += 1
            else:
                single_multi["single"] += 1

        print (u'\u2022' + " There is %d single questions (1 sentence) and %d multi questions (>1 sentence).\n" %
               (single_multi["single"], single_multi["multi"]))

        # Find how questions are located in terms of percentage of the context (25, 50, 75 and 100%)
        answer_located = defaultdict(int)
        answer_located_paragraphs = {0.25: defaultdict(int), 0.5: defaultdict(int),
                                     0.75: defaultdict(int), 1: defaultdict(int)}
        splits = [0.25, 0.5, 0.75, 1]

        for id, i in enumerate(data):
            if len(i["candidates"].split(",")) == 1:
                s_len = len(i["sentences"])
                s_id = int(i["candidates"])
                #print ("for s_len %d the answer sentence id is %d" % (s_len, s_id))
                for split in splits:
                    mult = None
                    if s_len == 3 and split == 0.25:
                        mult = 1
                    else:
                        mult = int(split*s_len)
                    if s_id <= mult:
                        #print ("Entered for split: %f" % (split))
                        answer_located[split] += 1
                        answer_located_paragraphs[split][s_len] += 1
                        break

        print (u'\u2022' + " The split how answers are located in the context (first 25%, first 50% etc.):")
        for k, v in answer_located.iteritems():
            print ("%s: %s (%.2f%%)" % (str(k).rjust(4), v, float(v)/single_multi["single"]*100))
            for kk, vv in answer_located_paragraphs[k].iteritems():
                print ("%s: %s (%.2f%%)" % (str(kk).rjust(2), vv, float(vv)/s_lens[kk]*100))

        print ("\n")

        # Check for each single sentence how many words between question and sentence answer are overlapping
        # Also, count why/what questions
        overlapping = []
        q_type_counts = {"what": 0, "why": 0, "who": 0, "where": 0, "when": 0, "how": 0, "other": 0}
        wt = nltk.RegexpTokenizer(r'\w+').tokenize

        for i in data:
            q_words = [x.lower() for x in wt(i["question"])]
            found_type = False

            for k, v in q_type_counts.iteritems():
                if k in q_words:
                    q_type_counts[k] += 1
                    found_type = True
                    break

            if not found_type:
                q_type_counts["other"] += 1

            if len(i["candidates"].split(",")) > 1:
                continue

            a_words = [x.lower() for x in wt(i["sentences"][int(i["candidates"])-1])]

            overlapping.append(float(len(set(q_words).intersection(a_words)))/len(q_words))

            #print ("q_words: %s\na_words: %s" % (q_words, a_words))

        print (u'\u2022' + " Overlapping words between q and sentence answer (only for single,"
                           " normalized by the length of the question):")
        print ("Min:  %.2f%% Max:   %.2f%%" % (min(overlapping)*100, max(overlapping)*100))
        print ("Mean: %.2f%% Median %.2f%%" % (mean(overlapping)*100, median(overlapping)*100))
        stdev = std(overlapping)*100
        print ("Std:  %.2f%%\n" % stdev)

        print (u'\u2022' + " Distribution of wh* types of questions:")
        for k, v in q_type_counts.iteritems():
            print ("%s: %s (%.2f%%)" % (str(k).rjust(5), v, float(v)/len(data)*100))


class DataGenerator:
    """
    Class to generate data from annotated paragraphs
    Data will be in form to be read by our framework
    """
    data_gen_filedir = "gen_data/"


    def __init__(self):
        pass

    def answer_extractor(self, answer_string):
        split_items = answer_string.split(",")

        return [int(i) for i in split_items]

    def generate_txt_file(self, data, filename):
        tsv_file = open(self.data_gen_filedir + filename, "w")

        for paragraph in data:
            question = paragraph["question"]
            answers = self.answer_extractor(paragraph["candidates"])

            #print ("Entire sample: %s" % paragraph)

            #print ("q: %s, answers: %s" % (question, answers))

            for i, j in enumerate(paragraph["sentences"]):
                if j == "":
                    print ("WARNING: it's empty! paragraph_id: %s in file: %s" %
                           (paragraph["paragraph_id"], paragraph["filename"]))
                else:
                    tsv_file.write(question.encode("utf-8") + "\t" + j.encode("utf-8") + "\t" +
                                   str(int(((i+1) in answers))) + "\n")


class DEPDataParser:
    """
    Class to prepare data for dependency parsing
    """

    def __init__(self):
        pass

    def generate_file(self, data, filename):
        dep_file = open(filename, "w")

        for paragraph in data:
            question = paragraph["question"]
            dep_file.write(question.encode("utf-8") + "\n")
            for i, j in enumerate(paragraph["sentences"]):
                if j == "":
                    print ("WARNING: it's empty! paragraph_id: %s in file: %s" %
                           (paragraph["paragraph_id"], paragraph["filename"]))
                else:
                    dep_file.write(j.encode("utf-8") + "\n")