#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tkinter import *
from matplotlib import pyplot
from PIL import ImageTk, Image
import numpy as np
import scipy.optimize as op
import boto3
import html
import collections
import itertools
import operator
import json


def clear_text(event):
    event.widget.delete(0, "end")


def choose_test(test_type, window, wave=1):
    global test
    test = test_type
    global is_First_wave
    is_First_wave = wave
    window.destroy()


def add_window(root=None):
    addwindow = Toplevel(root)
    addwindow.title("Add HIT")
    addwindow.grab_set()

    # Creating label and entry
    label_title = Label(addwindow, text="Title of the HIT")
    label_title.pack(side=TOP)
    title = Entry(addwindow, width=30)
    title.insert(0, "Guess all the characters in a sentence")
    title.bind("<Button-1>", clear_text)
    title.pack(side=TOP)

    label_description = Label(addwindow, text="Description of the HIT")
    label_description.pack(side=TOP)
    description = Entry(addwindow, width=30)
    description.insert(
        0,
        "Given a random sentence, find all the characters of the sentence one by one.",
    )
    description.bind("<Button-1>", clear_text)
    description.pack(side=TOP)

    label_keyword = Label(addwindow, text="Keywords for the HIT")
    label_keyword.pack(side=TOP)
    keyword = Entry(addwindow, width=30)
    keyword.insert(0, "Natural language, artificial intelligence, information theory")
    keyword.bind("<Button-1>", clear_text)
    keyword.pack(side=TOP)

    label_reward = Label(addwindow, text="Amount of money for the HIT")
    label_reward.pack(side=TOP)
    reward = Entry(addwindow, width=30)
    reward.insert(0, "0.1")
    reward.bind("<Button-1>", clear_text)
    reward.pack(side=TOP)

    label_maxAssign = Label(addwindow, text="Maximum assignments of the HIT")
    label_maxAssign.pack(side=TOP)
    maxAssign = Entry(addwindow, width=30)
    maxAssign.insert(0, "9")
    maxAssign.bind("<Button-1>", clear_text)
    maxAssign.pack(side=TOP)

    label_duration = Label(addwindow, text="Duration of the HIT")
    label_duration.pack(side=TOP)
    duration = Entry(addwindow, width=30)
    duration.insert(0, "604800")  # 2 days
    duration.bind("<Button-1>", clear_text)
    duration.pack(side=TOP)

    label_workingTime = Label(
        addwindow, text="Time available for the worker for the HIT"
    )
    label_workingTime.pack(side=TOP)
    workingTime = Entry(addwindow, width=30)
    workingTime.insert(0, "1200")  # 20 minutes
    workingTime.bind("<Button-1>", clear_text)
    workingTime.pack(side=TOP)

    label_approvalDelay = Label(addwindow, text="Time of approval of the HIT")
    label_approvalDelay.pack(side=TOP)
    approvalDelay = Entry(addwindow, width=30)
    approvalDelay.insert(0, "172800")  # 1 day
    approvalDelay.bind("<Button-1>", clear_text)
    approvalDelay.pack(side=TOP)

    validation = Button(
        addwindow,
        text="Validate",
        command=lambda: validate(
            title.get(),
            description.get(),
            keyword.get(),
            reward.get(),
            maxAssign.get(),
            duration.get(),
            workingTime.get(),
            approvalDelay.get(),
            addwindow,
        ),
    )
    validation.pack(side=TOP)


def validate(
    title,
    description,
    keyword,
    reward,
    maxAssign,
    duration,
    workingTime,
    approvalDelay,
    window,
):
    assert title, "Title must be indicated!"
    assert description, "You must provide a description for the HIT"
    assert keyword, "You must provide keyword(s) for the HIT"
    assert reward.replace(
        ".", "", 1
    ).isdigit(), "You must indicate the amount of reward"
    assert maxAssign.isnumeric(), "Maximum assignment must be provided"
    assert duration.isnumeric(), "You must indicate the assignment duration"
    assert workingTime.isnumeric(), "You must indicate the working time"

    print(
        "you have entered:",
        title,
        description,
        keyword,
        reward,
        maxAssign,
        duration,
        workingTime,
        approvalDelay,
    )

    if test == "gambling":
        if is_First_wave == 1:
            file = open(prefix + "HIT_list" + wave_number + ".txt", "a")
            wave_number_file = open(prefix + "wave_number_file.txt", "w")
            wave_number_file.write("1")
            wave_number_file.close()
            random_sentence = open("parse_text.txt", "r").read().splitlines()
        else:
            list_sentence = []  # to store sentences that have already been pubulished
            file = open(prefix + "HIT_list" + str(int(wave_number) + 1) + ".txt", "a")
            previous_result = open(
                prefix + "Submitted_result/submitted_result" + wave_number + ".txt", "r"
            )
            with open(prefix + "wave_number_file.txt", "r+") as wave_number_file:
                wave_number_file.seek(0)
                wave_number_file.write(str(int(wave_number) + 1))
                wave_number_file.truncate()
    else:
        random_sentence = open("parse_text.txt", "r").read().splitlines()
        file = open(prefix + "HIT_list.txt", "a")

    for i in range(12):  # Number of HIT
        ### Gambling test
        if test == "gambling":
            if is_First_wave == 1:
                # list_sentence=[]
                # list_sentence.append('"'+random_sentence[i*2+ii]+'"')
                new_hit = mturk.create_hit(
                    Title=title,
                    Description=description,
                    Keywords=keyword,
                    Reward=reward,  # Amount of money per HIT (in $)
                    MaxAssignments=int(
                        maxAssign
                    ),  # Number of slot available for worker
                    LifetimeInSeconds=int(duration),  # Time until the HIT end
                    AssignmentDurationInSeconds=int(workingTime),  # Time of work
                    AutoApprovalDelayInSeconds=int(approvalDelay),
                    Question=question.replace(
                        "replace sentence here", random_sentence[i]
                    ),
                    QualificationRequirements=[
                        {
                            "QualificationTypeId": "00000000000000000071",
                            "Comparator": "In",
                            "LocaleValues": [
                                {"Country": "GB"},
                                {"Country": "US"},
                                {"Country": "CA"},
                                {"Country": "AU"},
                            ],
                        }
                    ],
                )
                # question_form = question.replace("replace sentence here", ",".join(list_sentence))
            else:
                # list_start_character_index = []
                # list_capital = []
                while True:
                    tmp = previous_result.readline().split("&")
                    # print("\n\ncest tmp2",tmp[2][len('Answer: '):],"\n\n")
                    previous_sentence = tmp[2][len("Answer: ") :]
                    if previous_sentence not in list_sentence:
                        list_sentence.append(previous_sentence)
                        question_form = question.replace(
                            "replace sentence here", previous_sentence
                        )
                        break
                        # list_start_character_index.append(tmp[3])
                        # list_capital.append(tmp[4].split(",")[-1])

                question_form = question_form.replace(
                    "replace start character index here", tmp[3]
                )
                # question_form = question_form.replace("replace start fund here", ",".join(list_capital))
                new_hit = mturk.create_hit(
                    Title=title,
                    Description=description,
                    Keywords=keyword,
                    Reward=reward,  # Amount of money per HIT (in $)
                    MaxAssignments=int(
                        maxAssign
                    ),  # Number of slot available for worker
                    LifetimeInSeconds=int(duration),  # Time until the HIT end
                    AssignmentDurationInSeconds=int(workingTime),  # Time of work
                    AutoApprovalDelayInSeconds=int(approvalDelay),
                    Question=question_form,
                    QualificationRequirements=[
                        {
                            "QualificationTypeId": "00000000000000000071",
                            "Comparator": "In",
                            "LocaleValues": [
                                {"Country": "GB"},
                                {"Country": "US"},
                                {"Country": "CA"},
                                {"Country": "AU"},
                            ],
                        }
                    ],
                )
        # test_fichier = open("../test/test.html","w")
        # test_fichier.write(question_form)
        # test_fichier.close()

        ### Other test than gambling
        else:
            new_hit = mturk.create_hit(
                Title=title,
                Description=description,
                Keywords=keyword,
                Reward=reward,  # Amount of money per HIT (in $)
                MaxAssignments=int(maxAssign),  # Number of slot available for worker
                LifetimeInSeconds=int(duration),  # Time until the HIT end
                AssignmentDurationInSeconds=int(workingTime),  # Time of work
                AutoApprovalDelayInSeconds=int(approvalDelay),
                Question=question.replace("replace here", random_sentence[i]),
                # QualificationRequirements = [
                #   {
                #       'QualificationTypeId': '00000000000000000071',
                #       'Comparator': 'In',
                #       'LocaleValues': [
                #           {'Country': 'GB'}, {'Country': 'US'}, {'Country': 'CA'}, {'Country': 'AU'}
                #       ]
                #   }
                # ]
            )

        print("A new HIT has been created. You can preview it here:")
        print(
            "https://workersandbox.mturk.com/mturk/preview?groupId="
            + new_hit["HIT"]["HITGroupId"]
        )
        print("HITID = " + new_hit["HIT"]["HITId"] + " (Use to Get Results)")

        file.write(new_hit["HIT"]["HITId"] + "\n")

    file.close()

    window.destroy()


def result_window(root=None):
    resultwindow = Toplevel(root)
    resultwindow.title("Reviewing HITs")
    resultwindow.grab_set()

    submitted = Button(
        resultwindow, text="Retrieve all submitted answer", command=retrieve_all
    )
    submitted.pack(side=TOP)


# Only view submitted assigment
def retrieve_submitted():
    # if test=="gambling":
    #   if is_First_wave==1:
    #       file = open(prefix+"HIT_list"+wave_number+".txt","r")
    #       submitted_result = open(prefix+"Submitted_result/submitted_result"+wave_number+".txt","w")
    #   else:
    #       file = open(prefix+"HIT_list"+wave_number+".txt","r")
    #       submitted_result = open(prefix+"Submitted_result/submitted_result"+wave_number+".txt","w")
    # else:
    #   file = open(prefix+"HIT_list.txt","r")
    #   submitted_result = open(prefix+"Submitted_result/submitted_result.txt","w")

    # for HIT in file:
    #   print(HIT)
    #   answer = mturk.list_assignments_for_hit(HITId=HIT[:-1], AssignmentStatuses=['Submitted'])
    #   for i in answer['Assignments']:
    #       result = i["Answer"]
    #       result = html.unescape("AssignmentId: "+i["AssignmentId"] + "&WorkerId: " + i["WorkerId"] + "&Answer: " + result[result.find("<FreeText>")+len("<FreeText>"):result.find("</FreeText>")] +"\n")
    #       submitted_result.write(result)

    # file.close()
    # submitted_result.close()

    analyse_result()


def retrieve_all():
    # if test=="gambling":
    #     if is_First_wave==1:
    #         file = open(prefix+"HIT_list"+wave_number+".txt","r")
    #         submitted_result = open(prefix+"Submitted_result/submitted_result"+wave_number+".txt","w")
    #     else:
    #         file = open(prefix+"HIT_list"+wave_number+".txt","r")
    #         submitted_result = open(prefix+"Submitted_result/submitted_result"+wave_number+".txt","w")
    # else:
    #     file = open(prefix+"HIT_list.txt","r")
    #     submitted_result = open(prefix+"Submitted_result/submitted_result.txt","w")

    # for HIT in file:
    #     print(HIT)
    #     answer = mturk.list_assignments_for_hit(HITId=HIT[:-1], AssignmentStatuses=['Approved','Submitted'])
    #     for i in answer['Assignments']:
    #         result = i["Answer"]
    #         result = html.unescape("AssignmentId: "+i["AssignmentId"] + "&WorkerId: " + i["WorkerId"] + "&Answer: " + result[result.find("<FreeText>")+len("<FreeText>"):result.find("</FreeText>")] +"\n")
    #         submitted_result.write(result)

    # file.close()
    # submitted_result.close()

    analyse_resultV2()


def analyse_resultV2():
    # To count number of system error
    nb_error = 0

    if test != "gambling":
        if test == "simple":
            rate = []
        number_try = (
            []
        )  # number of tries for an index, number_try[0] means first characters
        list_repeating_letter = []  # list of answer that have bunch of repeating letter
        repeating_letter_cpt = 0  #
        list_guess = []
        nb_ppl_answer = []
        cpt_nb_ppl = 0
        list_plot = []
        somme = 0
    else:
        list_sentence = []  # to store sentence that are already retrieved
        bad_result = []  # to store bad result submitted by worker
        dict_answer = (
            {}
        )  # key = the sentence, value = list of dict of character and their percentage
        # the first element is the occurance of the sentence
    if test == "gambling":
        # file = open(prefix+"HIT_list"+wave_number+".txt","r")
        submitted_result = (
            open(
                prefix + "Submitted_result/submitted_result" + wave_number + ".txt", "r"
            )
            .read()
            .split("\n")[:-1]
        )
    else:
        # file = open(prefix+"HIT_list.txt","r")
        submitted_result = (
            open(prefix + "Submitted_result/submitted_result.txt", "r")
            .read()
            .split("\n")[:-1]
        )

    ####### Storing result in list #######
    # result represent one answer
    for result in submitted_result:
        tmp = result.split("&")
        if test != "gambling":
            length = len(tmp[2]) - len("Answer: ")
            if length == 0:
                nb_error += 1
                continue
            nb_ppl_answer.append(length)
        # print(tmp)
        if test == "simple":
            # print(tmp[2])
            rate.append(
                sum(int(x) for x in tmp[3] if x != "\n") / nb_ppl_answer[cpt_nb_ppl]
            )
            # list_guess.append(tmp[3])
            number_try = itertools.zip_longest(number_try, list(tmp[3]), fillvalue="2")
            number_try = map(",".join, number_try)
            # print(list(number_try))
            for i in range(1, len(tmp[4])):
                if tmp[4][i] == tmp[4][i - 1]:
                    repeating_letter_cpt += 1
                else:
                    repeating_letter_cpt = 0
                if repeating_letter_cpt > 6:
                    repeating_letter_cpt = 0
                    list_repeating_letter.append(result)
                    break
            cpt_nb_ppl += 1
        elif test == "hard":
            # print(tmp[3])
            # print(type(tmp[3]))
            # number_try += collections.Counter(map(int,tmp[3].split(",")))
            # list_guess.append(list(map(int,tmp[3].split(","))))
            number_try = itertools.zip_longest(
                number_try, tmp[3].split(","), fillvalue="0"
            )
            number_try = map(",".join, number_try)
            # print(list(number_try))
        else:
            error_cpt = 0  # counter for errors
            answer = tmp[4].split("|")  # answer represent the percentage of bet
            answer.pop()

            if wave_number == "1":
                list_capital = [1.0]
            else:
                temp = json.loads(
                    open(
                        prefix
                        + "Submitted_result/mean_result"
                        + str(int(wave_number) - 1)
                        + ".txt",
                        "r",
                    ).read()
                )
                if tmp[2][len("Answer: ") :] in temp:
                    list_capital = [temp[tmp[2][len("Answer: ") :]][1][-1]]
                else:
                    continue

            # Count there is how much answer for a sentence
            if tmp[2][len("Answer: ") :] not in dict_answer:
                dict_answer[tmp[2][len("Answer: ") :]] = [1]
            else:
                dict_answer[tmp[2][len("Answer: ") :]][0] += 1

            for i in answer:
                tmp2 = i.split(",")
                tmp_list = []
                tmp_dict = {}
                tmp_list.append(tmp2[0])  # the right character
                for i in range(1, len(tmp2)):
                    # else:
                    tmp_dict[tmp2[i][0]] = float(
                        tmp2[i][1:]
                    )  # separate the letter and the percentage, "A":50
                tmp_list.append(tmp_dict)
                # print(list_capital[-1])
                if tmp_list[0] in tmp_list[1]:
                    list_capital.append(
                        27 * list_capital[-1] * tmp_list[1][tmp_list[0]] / 100.0
                    )
                    # list_capital *= tmp_list[1][tmp_list[0]]/100.0
                else:
                    list_capital.append(list_capital[-1] * 0.01)
                    error_cpt = error_cpt + 1
                    # list_capital *= 0.01
            if (
                error_cpt > 2
            ):  # We don't consider the answer if the error is greater than a treshold
                # print(tmp[2][len("Answer: "):])
                dict_answer[tmp[2][len("Answer: ") :]][0] -= 1
                continue

            # print(list_capital)
            list_capital.pop(0)
            if len(dict_answer[tmp[2][len("Answer: ") :]]) == 1:
                dict_answer[tmp[2][len("Answer: ") :]].append(list_capital)
            else:
                dict_answer[tmp[2][len("Answer: ") :]][1] = list(
                    map(
                        operator.add,
                        dict_answer[tmp[2][len("Answer: ") :]][1],
                        list_capital,
                    )
                )
            # print(dict_answer)
    # print(dict_answer)
    # exit()
    ####### Analysing result #######
    if test == "simple":
        mean = sum(rate) / len(rate)
        print("The mean value of answers:", mean)
        minimum_rate = (
            mean - 0.4 * mean
        )  # If rate of an answer is less than 40% of the mean valu, we have to pay attention
        print("minimum:", minimum_rate)

        special_attention = open(prefix + "Submitted_result/special_attention.txt", "w")
        special_attention.write("######## REPEATING LETTER ######## \n")
        special_attention.write("\n".join(list_repeating_letter))
        special_attention.write("\n\n ######## SPECIAL ATTENTION ########\n")
        for index, i in enumerate(rate):
            if i < minimum_rate:
                special_attention.write(submitted_result[index])

        special_attention.close()

        number_try = list(number_try)

        for i in number_try:
            i = collections.Counter(i.split(","))
            del i["2"]
            number_of_answer = sum(i.values())
            list_guess.append(
                {k: v / number_of_answer for k, v in i.items()}
            )  # On regarde que les bonne réponse
            # print(list_guess)
        for index, i in enumerate(list_guess):
            list_plot.append(-sum(np.log(prob) * prob for prob in i.values()))

        pyplot.plot(list_plot)
        pyplot.show()
        # print(list_guess)
    elif test == "hard":
        # dict_occurrence = list(set(nb_ppl_answer))
        # dict_occurrence.sort()
        # dict_occurrence = {key:sum(v>=key for v in nb_ppl_answer) for key in dict_occurrence}
        # dict_occurrence = sorted(dict_occurrence.items()) # (length of the answer, number of answer who have length more thant that)
        # print(dict_occurrence)

        number_try = list(
            number_try
        )  # number_try[0] means number of tries for the first character
        for i in number_try:
            i = collections.Counter(i.split(","))
            del i["0"]  # 0 are useless
            number_of_answer = sum(i.values())
            # print(number_of_answer)
            list_guess.append({int(k): v / number_of_answer for k, v in i.items()})
        # print(len(list_guess))

        # # Vérifie si tous les lignes font 1
        # a=[]
        # somme = 0
        # for i in list_guess:
        #       for key,value in i.items():
        #               somme = somme + float(value)
        #       a.append(somme)
        #       somme = 0
        # print(a)

        # Plot h en fonction de nb de lettre

        list_upper = [np.log2(27)]
        list_lower = [np.log2(27)]

        # print(list_guess)
        for i in list_guess:
            list_upper.append((-sum(np.log(prob) * prob for prob in i.values())))
            i = collections.OrderedDict(sorted(i.items()))
            lower_freq = 0
            for cpt in range(1, 28):
                if cpt in i:
                    if cpt + 1 in i:
                        lower_freq += cpt * (i[cpt] - i[cpt + 1]) * np.log(cpt)
                    else:
                        lower_freq += cpt * i[cpt] * np.log(cpt)
                else:
                    if cpt + 1 in i:
                        lower_freq += cpt * -i[cpt + 1] * np.log(cpt)
            list_lower.append(lower_freq)

        print(len(list_upper))
        print(len(list_lower))
        # Minimizing the ansazt function
        x0 = np.array([0, 0, 0])
        x = np.arange(1, len(list_upper) + 1)
        # x = np.linspace(1,len(list_upper),len(list_upper))
        matlab = open("matlab.txt", "w")
        matlab.write("[" + ",".join(str(x) for x in list_upper) + "]\n")
        matlab.write("[" + ",".join(str(x) for x in list_lower) + "]")
        y_upper = np.array(list_upper)
        y_lower = np.array(list_lower)

        ########### Minimization with f1 ansatz ###########

        #### Using least_squres optimization
        res_upper = op.least_squares(
            func, x0, args=(x, y_upper), loss="cauchy", f_scale=0.1
        )
        res_lower = op.least_squares(
            func, x0, args=(x, y_lower), loss="cauchy", f_scale=0.1
        )
        f_upper = ansatz_least(res_upper.x, x)
        f_lower = ansatz_least(res_lower.x, x)
        print("res_upper:", res_upper.x)
        print("res_lower:", res_lower.x)
        pyplot.figure(1)
        pyplot.plot(list_upper, "o", label="Upper bound data")
        pyplot.plot(list_lower, "+", label="Lower bound data")
        pyplot.plot(
            f_upper,
            label="Fitted upper bound: A={:5.3f}, beta={:5.3f}, h={:5.3f}".format(
                res_upper.x[0], res_upper.x[1], res_upper.x[2]
            ),
        )
        pyplot.plot(
            f_lower,
            label="Fitted lower bound: A={:5.3f}, beta={:5.3f}, h={:5.3f}".format(
                res_lower.x[0], res_lower.x[1], res_lower.x[2]
            ),
        )
        pyplot.legend()
        pyplot.suptitle("Least squares method")
        # pyplot.show()

        #### Using curve_fit optimization
        res_upper = op.curve_fit(ansatz_curve, x, y_upper)
        res_lower = op.curve_fit(ansatz_curve, x, y_lower)
        f_upper = ansatz_curve(x, *res_upper[0])
        f_lower = ansatz_curve(x, *res_lower[0])
        print("res_upper:", res_upper[0])
        print("res_lower:", res_lower[0])

        pyplot.figure(2)
        pyplot.plot(list_upper, "o", label="Upper bound data")
        pyplot.plot(list_lower, "+", label="Lower bound data")
        pyplot.plot(
            f_upper,
            label="Fitted upper bound: A={:5.3f}, beta={:5.3f}, h={:5.3f}".format(
                res_upper[0][0], res_upper[0][1], res_upper[0][2]
            ),
        )
        pyplot.plot(
            f_lower,
            label="Fitted lower bound: A={:5.3f}, beta={:5.3f}, h={:5.3f}".format(
                res_lower[0][0], res_lower[0][1], res_lower[0][2]
            ),
        )
        pyplot.legend()
        pyplot.suptitle("Curve fit method")
        pyplot.show()

    else:
        tmp = dict(dict_answer)
        for i in dict_answer:
            if tmp[i][0] == 0:
                # print(i)
                del tmp[i]
        dict_answer = tmp
        for i in dict_answer:
            # print(i)
            dict_answer[i][1] = list(
                map(lambda x: x / dict_answer[i][0], dict_answer[i][1])
            )

        mean_result = open(
            prefix + "Submitted_result/mean_result" + wave_number + ".txt", "w"
        )
        mean_result.write(json.dumps(dict_answer))  # use `json.loads` to do the reverse
        mean_result.close()

        analyse_gambling()


def analyse_gambling():
    answer = json.loads(
        open(prefix + "Submitted_result/mean_result1" + ".txt", "r").read()
    )

    for i in range(2, int(wave_number) + 1):
        tmp = json.loads(
            open(prefix + "Submitted_result/mean_result" + str(i) + ".txt", "r").read()
        )
        diff = set(answer) - set(tmp)
        for i in diff:
            del answer[i]
        for key, value in tmp.items():
            answer[key][1] = (
                answer[key][1] + value[1]
            )  # concat the previous capital with the following

    # print(answer)
    # for i in answer:
    # print(i)
    tmp = []
    for key, value in answer.items():
        tmp.append(
            [
                (1 - (1 / (n + 1)) * (np.log(s) / np.log(27))) * np.log2(27)
                for n, s in enumerate(answer[key][1])
            ]
        )

    print(len(tmp))

    list_plot = tmp[0]
    for i in range(1, len(tmp)):
        list_plot = list(map(operator.add, list_plot, tmp[i]))

    list_plot = list(map(lambda x: x / len(tmp), list_plot))
    print(list_plot)
    pyplot.plot(list_plot)
    # pyplot.suptitle("Entropy rate variation (Cover & King)")
    pyplot.xlabel("Number of character")
    pyplot.ylabel("Entropy rate(bits/character)")
    # x = np.arange(1,len(list_plot)+1)
    # res = op.curve_fit(ansatz_curve,x,np.array(list_plot))
    # print(res)
    # f = ansatz_curve(x,*res[0])
    # pyplot.plot(f,label='Fitted upper bound: A={:5.3f}, beta={:5.3f}, h={:5.3f}'.format(res[0][0], res[0][1], res[0][2]))
    pyplot.show()


def func(variable, x, y):
    """function to be minimized"""
    return ansatz_least(variable, x) - y


def ansatz_least(variable, x):
    return variable[0] * x ** (variable[1] - 1) + variable[2]


def ansatz_curve(x, A, beta, h):
    return A * x ** (beta - 1) + h


if __name__ == "__main__":
    # endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
    endpoint_url = "https://mturk-requester.us-east-1.amazonaws.com"

    print("You are using endpoint_url= ", endpoint_url)

    # Connecting to the account
    mturk = boto3.client(
        "mturk",
        aws_access_key_id="XXXXXXX",
        aws_secret_access_key="XXXXXXXXXXX",
        region_name="us-east-1",
        endpoint_url=endpoint_url,
    )
    #'https://mturk-requester.us-east-1.amazonaws.com' -> to publish on the official site
    # "https://mturk-requester-sandbox.us-east-1.amazonaws.com" -> to test before publishing

    # Choose what kind of test we want: simple, hard, gambling

    window = Tk()
    window.title("Choose type of test")

    button = Button(
        window,
        text="simple",
        command=lambda: choose_test("simple", window),
        compound=BOTTOM,
        height=5,
        width=15,
    )
    button.pack(side=LEFT)

    button2 = Button(
        window,
        text="hard",
        command=lambda: choose_test("hard", window),
        compound=BOTTOM,
        height=5,
        width=15,
    )
    button2.pack(side=LEFT)

    button3 = Button(
        window,
        text="Gambling wave 1",
        command=lambda: choose_test("gambling", window),
        compound=BOTTOM,
        height=5,
        width=15,
    )
    button3.pack(side=LEFT)

    button3 = Button(
        window,
        text="Gambling other wave",
        command=lambda: choose_test("gambling", window, 2),
        compound=BOTTOM,
        height=5,
        width=15,
    )
    button3.pack(side=LEFT)

    window.mainloop()

    if test == "simple":
        prefix = "simple_test/"
        question = open("index_simple.html", "r").read()

    elif test == "hard":
        prefix = "hard_test/"
        question = open("index_hard.html", "r").read()

    else:
        prefix = "gambling_test/"
        if is_First_wave == 1:
            question = open(
                "index_gambling1.html", "r"
            ).read()  # HTML to render when it's the first wave
            wave_number = str(1)
        else:
            question = open("index_gambling2.html", "r").read()
            wave_number = open(prefix + "wave_number_file.txt", "r").read()

    question = (
        '<HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">\
                \n<HTMLContent><![CDATA['
        + question
        + "]]> </HTMLContent> <FrameHeight>450</FrameHeight> </HTMLQuestion>"
    )

    window = Tk()
    window.title("Main window")
    im = Image.open("plus.png").resize((100, 100))
    render = ImageTk.PhotoImage(im)

    button = Button(
        window,
        text="Create a HIT",
        command=lambda: add_window(window),
        compound=BOTTOM,
        height=5,
        width=10,
    )  # ,image=render)
    button.pack(side=LEFT)

    # button2 = Button(window,text="Delete a HIT",command=lambda:add_window(window),compound=BOTTOM)#,height=255,width=255)#,image=render)
    # button2.pack(side=LEFT)

    button3 = Button(
        window,
        text="Retrieve results",
        command=lambda: result_window(window),
        compound=BOTTOM,
        height=5,
        width=10,
    )  # ,image=render)
    button3.pack(side=LEFT)

    window.mainloop()

    # how to retrieve answer:
    # a=mturk.list_assignments_for_hit(HITId="HITid")
    # a['Assignments'][0]['Answer'] Perhaps [1] or other if there are more than 1 assigment
