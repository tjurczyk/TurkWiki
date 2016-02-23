# -*- coding: utf-8 -*-

import re
import random
from collections import defaultdict

import nltk
from numpy import mean, median, std

import csv

csv_filename = "batch-results-paraphrase/batch1-paraphrase.csv"

csv_file = open(csv_filename)
csv_data = csv.reader(csv_file)

d = []
reg_exp = re.compile('[^:]+: ([^<]+)[^:]+: (.*)')
stopwords = set(nltk.corpus.stopwords.words('english'))

for i, row in enumerate(csv_data):
    if i == 0:
        input_index = row.index('Input.content')
        parap_index = row.index('Answer.ParaphraseQuestionBox')
        continue

    matches = reg_exp.search(unicode(row[input_index], "utf-8"))
    question = matches.group(1)
    sentence = matches.group(2)

    paraphrase = unicode(row[parap_index], "utf-8")

    print ("\nSentence: %s\nQuestion: %s\nParaphrase: %s\n" % (sentence, question, paraphrase))
    d.append({'sentence': sentence, 'question': question, 'paraphrase': paraphrase})

wt = nltk.RegexpTokenizer(r'\w+').tokenize
for i in d:
    q_words = [x.lower() for x in wt(i["question"]) if x not in stopwords]
    s_words = [x.lower() for x in wt(i["sentence"]) if x not in stopwords]
    p_words = [x.lower() for x in wt(i["paraphrase"]) if x not in stopwords]

    q_set = set(q_words)
    s_set = set(s_words)
    p_set = set(p_words)

    #print ("old intersection: %s\nnew intersection: %s\n" % (q_set.intersection(s_set), p_set.intersection(s_set)))

    old_overlapping = (float(len(q_set.intersection(s_set)))/len(q_words))
    new_overlapping = (float(len(p_set.intersection(s_set)))/len(p_words))

    #print ("old: %.2f, new: %.2f,  diff: %.2f" % (old_overlapping*100, new_overlapping*100, new_overlapping*100-old_overlapping*100))