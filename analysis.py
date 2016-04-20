import pickle
from pprint import pprint

f = open("analysis/q_answers.pickle", "rb")
predictions = pickle.load(f)
f = open("analysis/test_list_for_analysis.pickle", "rb")
test_dict = pickle.load(f)
f = open("analysis/is_answer-test.pickle", "rb")
is_answer = pickle.load(f)


print ("Len of predictions: %d, len of test_dict: %d" % (len(predictions), len(test_dict)))
print ("Correctly predicted: %d" % len([1 for x in predictions if x == 1]))
print ("Question with answers in data set: %d" % (len([1 for x in is_answer if x == 1])))
print ("test_dict has keys of: %s\n\n" % test_dict[0].keys())


# print ("test_dict:")
# pprint(test_dict)
# exit(0)


######################
#
# Question length

q_len = {}

for id, i in enumerate(test_dict):
    if is_answer[id] == 0:
        continue

    if i["q_len"] not in q_len:
        q_len[i["q_len"]] = {0: 0, 1: 0}

    q_len[i["q_len"]][predictions[id]] += 1

q_len_answered = {}
q_len.pop(2, None)

q_len_2 = {}
summ = 0
for k, v in q_len.iteritems():
    val5 = k / 5
    if val5 not in q_len_2:
        q_len_2[val5] = {0: 0, 1:0, "all": 0}

    q_len_2[val5][1] += v[1]
    q_len_2[val5][0] += v[0]
    q_len_2[val5]["all"] += v[1] + v[0]

for k, v in q_len_2.iteritems():
    q_len_2[k]["answered"] = float(v[1])/(v[1]+v[0])


# for k, v in q_len.iteritems():
#     q_len_answered[k] = float(q_len[k][1]) / (q_len[k][1] + q_len[k][0])

print ("Question length")
print ("Range      #        ACC")
for k, v in q_len_2.iteritems():
    fr = k*5
    print ((str(fr) + "-" + str(fr+4)).ljust(11, " ") + (str(v["all"])).ljust(9, " ") + "%.4f" % (v["answered"]))

# pprint(q_len_2)

######################
# Sentence length

s_len_mean = 0
s_len = {}
for id, i in enumerate(test_dict):
    if is_answer[id] == 0:
        continue

    # print ("Working on slen: %d" % i["s_len"])
    s_len_mean += i["s_len"]
    if i["s_len"] not in s_len:
        s_len[i["s_len"]] = {0: 0, 1: 0}

    s_len[i["s_len"]][predictions[id]] += 1

s_len_answered = {}
s_len_2 = {}

for k, v in s_len.iteritems():
    val5 = k / 25
    if val5 not in s_len_2:
        s_len_2[val5] = {0: 0, 1:0, "all": 0}

    s_len_2[val5][1] += v[1]
    s_len_2[val5][0] += v[0]
    s_len_2[val5]["all"] += v[1] + v[0]

for k, v in s_len_2.iteritems():
    s_len_2[k]["answered"] = float(v[1])/(v[1]+v[0])

# print ("s_len arr: ")
# pprint (s_len)

print ("\n\nSection length")
print ("Range      #        ACC")
for k, v in s_len_2.iteritems():
    fr = k*25
    print ((str(fr) + "-" + str(fr+24)).ljust(11, " ") + (str(v["all"])).ljust(9, " ") + "%.4f" % (v["answered"]))

######################
# Question type

q_type = {}

for id, i in enumerate(test_dict):
    if is_answer[id] == 0:
        continue

    if "q_types" not in i:
        if "other" not in q_type:
            q_type["other"] = {0: 0, 1: 0}
        q_type["other"][predictions[id]] += 1

    else:
        for t in i["q_types"]:
            if t not in q_type:
                q_type[t] = {0: 0, 1: 0}

            q_type[t][predictions[id]] += 1

q_type_answered = {}

for k, v in q_type.iteritems():
    q_type_answered[k] = {1: v[1], 0: v[0]}
    q_type_answered[k]["answered"] = float(v[1])/(v[0]+v[1])

# print ("q_type arr: ")
# pprint (q_type_answered)

print ("\n\nQuestion Type")
print ("Type       #        ACC")
for k, v in q_type_answered.iteritems():
    fr = k*5
    print ((k).ljust(11, " ") + (str(v[1]+v[0])).ljust(9, " ") + "%.4f" % (v["answered"]))


######################
# Genera

genera = {}

for id, i in enumerate(test_dict):
    if is_answer[id] == 0:
        continue
    if i["genera"] not in genera:
        genera[i["genera"]] = {0: 0, 1: 0}

    genera[i["genera"]][predictions[id]] += 1

genera_answered = {}

for k, v in genera.iteritems():
    genera_answered[k] = {1: v[1], 0: v[0]}
    genera_answered[k]["answered"] = float(v[1])/(v[0]+v[1])

# print ("genera arr: ")
# pprint (genera_answered)

print ("\n\nGenera ")
print ("Name               #           ACC")
for k, v in genera_answered.iteritems():
    print ((k).ljust(19, " ") + (str(v[0]+v[1])).ljust(12, " ") + "%.4f" % (v["answered"]))


######################
# is Paraphrased

isp = {True: {0: 0, 1: 0}, False: {0: 0, 1: 0}}

for id, i in enumerate(test_dict):
    if is_answer[id] == 0:
        continue
    # print ("Working on slen: %d" % i["s_len"])

    isp[i["q_is_paraphrase"]][predictions[id]] += 1

isp_answered = {}

for k, v in isp.iteritems():
    isp_answered[k] = {1: v[1], 0: v[0]}
    isp_answered[k]["answered"] = float(v[1])/(v[0]+v[1])

print ("isp_answered arr: ")
pprint (isp_answered)

print ("\n\nParaphrase or not")
print ("isP        #        ACC")
for k, v in isp_answered.iteritems():
    print ((str(k)).ljust(11, " ") + (str(v[1]+v[0])).ljust(9, " ") + "%.4f" % (v["answered"]))


######################
# is Paraphrased

#questions not answered

q_na = []

for id, i in enumerate(test_dict):
    if is_answer[id] == 0:
        continue

    if predictions[id] == 0:
        q_na.append(test_dict[id]["question"])

print ("Questions not answered:")
for i in q_na:
    print i