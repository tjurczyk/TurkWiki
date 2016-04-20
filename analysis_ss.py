import pickle
from pprint import pprint
import numpy

# use 'test' or 'val'
split_name = "test"


#########################

f = open("analysis_ss/y_" + split_name + "_predictions.pickle", "rb")
predictions = pickle.load(f)
f = open("analysis_ss/y_" + split_name + ".pickle", "rb")
labels = pickle.load(f)
f = open("analysis_ss/" + split_name + "_list_for_analysis.pickle", "rb")
test_dict = pickle.load(f)

answered_or_not = []
# Parse predictions and create answered_or_not
index_begin = 0
mrr = 0
for question_set in labels:
    index_end = index_begin + len(question_set)

    predictions_slice = predictions[index_begin:index_end].flatten().tolist()

    xx = zip(question_set, predictions_slice)
    xx = sorted(xx, key=lambda tup: tup[1], reverse=True)

    for id, x in enumerate(xx):
        if x[0] == 1:
            mrr += float(1)/(id+1)
            answered_or_not.append(float(1)/(id+1))
            break

    index_begin = index_end

# exit(0)
mrr = float(mrr)/len(labels)
predictions = answered_or_not

print ("mrr: %f" % mrr)

print ("Len of predictions: %d, len of test_dict: %d" % (len(predictions), len(test_dict)))
print ("Correctly predicted: %d" % len([1 for x in predictions]))
print ("test_dict has keys of: %s\n\n" % test_dict[0].keys())

######################
#
# Question length

q_len = {}

for id, i in enumerate(test_dict):
    if i["q_len"] not in q_len:
        q_len[i["q_len"]] = {"val": 0, "number": 0}

    q_len[i["q_len"]]["val"] += predictions[id]
    q_len[i["q_len"]]["number"] += 1

# pprint (q_len)


print ("Question length")
print ("Range      #        ACC")
for k, v in q_len.iteritems():
    print ((str(k)).ljust(11, " ") + str(v["number"]).ljust(9, " ") + "%.4f" % (v["val"]/v["number"]))


######################
# Sentence length

s_len_mean = 0
s_len = {}
for id, i in enumerate(test_dict):
    s_len_mean += i["s_len"]
    if i["s_len"] not in s_len:
        s_len[i["s_len"]] = {"val": 0, "number": 0}

    s_len[i["s_len"]]["val"] += predictions[id]
    s_len[i["s_len"]]["number"] += 1

print ("\n\nSection length")
print ("Range      #        ACC")
for k, v in s_len.iteritems():
    fr = k
    print ((str(fr) + "-" + str(fr+4)).ljust(11, " ") + (str(v["number"])).ljust(9, " ") + "%.4f" % (v["val"]/v["number"]))

######################
# Question type

q_type = {}

for id, i in enumerate(test_dict):
    if "q_types" not in i:
        if "other" not in q_type:
            q_type["other"] = {"val": 0, "number": 0}
        q_type["other"]["number"] += 1
        q_type["other"]["val"] += predictions[id]

    else:
        for t in i["q_types"]:
            if t not in q_type:
                q_type[t] = {"val": 0, "number": 0}

            q_type[t]["number"] += 1
            q_type[t]["val"] += predictions[id]

print ("\n\nQuestion Type")
print ("Type       #        ACC")
for k, v in q_type.iteritems():
    print ((k).ljust(11, " ") + (str(v["number"])).ljust(9, " ") + "%.4f" % (v["val"]/v["number"]))

######################
# Genera

genera = {}

for id, i in enumerate(test_dict):
    if i["genera"] not in genera:
        genera[i["genera"]] = {"val": 0, "number": 0}

    genera[i["genera"]]["val"] += predictions[id]
    genera[i["genera"]]["number"] += 1

print ("\n\nGenera ")
print ("Name               #           ACC")
for k, v in genera.iteritems():
    print ((k).ljust(19, " ") + (str(v["number"])).ljust(12, " ") + "%.4f" % (v["val"]/v["number"]))

######################
# is Paraphrased

isp = {True: {"val": 0, "number": 0}, False: {"val": 0, "number": 0}}

for id, i in enumerate(test_dict):
    # print ("Working on slen: %d" % i["s_len"])
    try:
        isp[i["q_is_paraphrase"]]["val"] += predictions[id]
        isp[i["q_is_paraphrase"]]["number"] += 1
    except KeyError:
        pprint(i)
        exit(1)

print ("\n\nParaphrase or not")
print ("isP        #        ACC")
for k, v in isp.iteritems():
    print ((str(k)).ljust(11, " ") + (str(v["number"])).ljust(9, " ") + "%.4f" % (v["val"]/v["number"]))