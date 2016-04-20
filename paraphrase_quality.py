# -*- coding: utf-8 -*-

import re
import random
from collections import defaultdict

import nltk
from numpy import mean, median, std

import csv

####
# INPUT FOR THE SCRIPT
####

csv_filename = "batch-results-paraphrase/batch101sq-paraphrase.csv"

####

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
    sentences = matches.group(2).split("</br>")

    paraphrase = unicode(row[parap_index], "utf-8")

    # print ("\nSentences: %s\nQuestion: %s\nParaphrase: %s\n" % (sentences, question, paraphrase))
    d.append({'sentences': sentences, 'question': question, 'paraphrase': paraphrase})

wt = nltk.RegexpTokenizer(r'\w+').tokenize
difference_sum = 0.0
old_sum_question = 0.0
old_sum_sentence = 0.0

new_sum_paraphrase = 0.0
new_sum_sentence = 0.0

for i in d:
    q_words = [x.lower() for x in wt(i["question"]) if x not in stopwords]
    q_set = set(q_words)
    p_words = [x.lower() for x in wt(i["paraphrase"]) if x not in stopwords]
    p_set = set(p_words)

    for s in i["sentences"]:
        s_words = [x.lower() for x in wt(s) if x not in stopwords]
        if len(s_words) == 0:
            continue
        # print ("Sentences: %s" % i["sentences"])
        s_set = set(s_words)

        #print ("old intersection: %s\nnew intersection: %s\n" % (q_set.intersection(s_set), p_set.intersection(s_set)))

        old_overlapping_question = (float(len(q_set.intersection(s_set)))/len(q_words))
        old_overlapping_sentence = (float(len(q_set.intersection(s_set)))/len(s_words))

        new_overlapping_paraphrase = (float(len(p_set.intersection(s_set)))/len(p_words))
        new_overlapping_sentence = (float(len(p_set.intersection(s_set)))/len(s_words))

        old_sum_question += old_overlapping_question*100
        old_sum_sentence += old_overlapping_sentence*100

        new_sum_paraphrase += new_overlapping_paraphrase*100
        new_sum_sentence += new_overlapping_sentence*100

    #difference_sum += (new_overlapping*100-old_overlapping*100)


    #print ("old: %.2f, new: %.2f,  diff: %.2f" % (old_overlapping*100, new_overlapping*100, new_overlapping*100-old_overlapping*100))

old_sum_question /= len(d)
old_sum_sentence /= len(d)
new_sum_paraphrase /= len(d)
new_sum_sentence /= len(d)

print ("Avg old overlapping by q: %.2f\nAvg old overlapping by s: %.2f" % (old_sum_question, old_sum_sentence))
print ("F1 for old overlapping: %.2f" % (2*old_sum_question*old_sum_sentence/(old_sum_question+old_sum_sentence)))

print ("\nAvg new overlapping by q: %.2f\nAvg new overlapping by s: %.2f" % (new_sum_paraphrase, new_sum_sentence))
print ("F1 for new overlapping: %.2f" % (2*new_sum_paraphrase*new_sum_sentence/(new_sum_paraphrase+new_sum_sentence)))

#print ("Average of old overlappings: %.2f" % (old_sum/len(d)))
#print ("Average of new overlappings: %.2f" % (new_sum/len(d)))
#print ("Average of all changes: %.2f" % (difference_sum/len(d)))