####
# INPUT FOR THE SCRIPT
####

work_dir = "wikiqa_ss/"
#wikiqa_splits = ["WikiQASent-train.txt", "WikiQASent-dev.txt", "WikiQASent-test.txt"]
wikiqa_splits = ["WikiQASent-train"]

####

for split in wikiqa_splits:
    fi = open(work_dir + split + ".txt", "r")
    q_with_answers = []
    number_of_q = 0
    number_of_lines = []

    has_answer = False
    question = None
    lines = []

    dep_file = open(work_dir + split + "-to_parse.txt", "w")
    sample_file = open(work_dir + split + "-ss.txt", "w")

    for line in fi.readlines():
        q, s, label = line.split("\t")

        if label.strip() == "1" and question == q:
            has_answer = True

        if question == None:
            number_of_q += 1
            question = q

        if question != q:
            # new question, check previous and write if necessary

            print ("Here for:\nQ: %s\nID: %d\nList: \nhas_answer: %s\n" % (question, number_of_q,has_answer))

            if has_answer == True:
                # Write sample to samples file
                for l in lines:
                    sample_file.write(l)

                # Write sample to dep file
                dep_file.write(question + "\n")
                for l in lines:
                    dep_file.write(l.split("\t")[1] + "\n")


                number_of_lines.append(len(lines))
                q_with_answers.append(number_of_q)

            number_of_q += 1
            question = q
            lines = []

            if label.strip() == "1":
                has_answer = True
            else:
                print ("In here for id: %s" % number_of_q)
                has_answer = False

        lines.append(line)

    if has_answer:
        # the last one
        q_with_answers.append(number_of_q)
        # Write sample to samples file
        for l in lines:
            sample_file.write(l)

        # Write sample to dep file
        dep_file.write(question + "\n")
        for l in lines:
            dep_file.write(l.split("\t")[1] + "\n")

    print ("length of q_with_answers for %s: %d" % (split, len(q_with_answers)))
    # print ("len of questions for %s: %d" % (split, number_of_q))
    # print ("q_with_answers: %s" % q_with_answers)
    # print ("lines to write: %s" % number_of_lines)
    # print ("len of lines gto write: %s" % len(number_of_lines))