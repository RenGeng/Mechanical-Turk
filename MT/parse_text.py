import re
import os
import sys

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase



# assert len(sys.argv) == 3,"Enter the minimum and maximum length that you want to parse."

parsed = open("parse_text.txt","w")

for file_name in os.listdir("../1989/"):
    text = open("../1989/"+file_name,"r").read().split(".")
    for i in text:
        i = i.replace("\"","")
        if "'S" in i.upper() or "S'" in i.upper() or "MC" in i.upper() or "CORP " in i.upper():
            continue
        tmp = [word for word in i.split() if word.istitle() or word.isupper()]
        if len(tmp) > 1:
            continue
        # print(tmp)
        for test in tmp:
            b=0
            if len([i for i in test if i.isupper()]) > 1:
                # print([i for i in test if i.isupper()])
                b+=1
                break
        if b>0:
            continue
        i = i.replace(",","")[2:]
        if not bool(re.search('[-`/()@:;&?_{|}`~\\/*+&%#^=\'\d]+',i)) and len(i)==int(sys.argv[1]):# and len(i)<=int(sys.argv[2]):
            if i[0].isupper() and "'" not in i:
                parsed.write(decontracted(i)+"\n")

parsed.close()