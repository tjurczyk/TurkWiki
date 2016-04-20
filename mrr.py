import pickle
import sys
# from pprint import pprint

if len(sys.argv) != 3:
    print ("Use with two arguments: python mrr.py [y_filename] [y_predictions_filename]")
    exit(0)

y_file = sys.argv[1]
y_predictions_file = sys.argv[2]

f = open(y_file, "rb")
l = pickle.load(f)
f = open(y_predictions_file, "rb")
p = pickle.load(f)
index_begin = 0

# pprint(l)
# pprint(p)
ss = 0

for id, i in enumerate(l):
    ss += len(i)

print ("Len of y: %d, pred: %d" % (ss, len(p)))


mrr = 0

# mrr
for question_set in l:
    index_end = index_begin + len(question_set)
    predictions_slice = p[index_begin:index_end].flatten().tolist()

    # Pair label-prediction and sort by prediction descending order
    xx = zip(question_set, predictions_slice)
    xx = sorted(xx, key=lambda tup: tup[1], reverse=True)


    for id, x in enumerate(xx):
        if x[0] == 1:
            mrr += float(1)/(id+1)
            break

    index_begin = index_end


print ("mrr: %.4f" % (float(mrr)/len(l)))

av_prec = 0
index_begin = 0
# map
for question_set in l:
    index_end = index_begin + len(question_set)
    predictions_slice = p[index_begin:index_end].flatten().tolist()

    correct_answers = len([1 for x in question_set if x == 1])

    xx = zip(question_set, predictions_slice)
    xx = sorted(xx, key=lambda tup: tup[1], reverse=True)

    # print ("Sorted: %s" % xx)

    correct = 0
    wrong = 0
    av_prec_i = 0

    for id, x in enumerate(xx):
        if x[0] == 1:
            correct += 1
        else:
            wrong += 1

        if x[0] == 1:
            av_prec_i += float(correct)/(correct + wrong)

        if correct == correct_answers:
            break

    # print ("av_prec_i: %f" % av_prec_i)
    # print ("av_prec_i/correct: %f" % float(av_prec_i/correct_answers))
    # raw_input()

    if correct_answers > 0:
        av_prec += av_prec_i/correct_answers

    index_begin = index_end

print ("map: %.4f" % (float(av_prec)/len(l)))