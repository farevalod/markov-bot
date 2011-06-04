import random;
import sys;
import re;

stopword = "\n" # Since we split on whitespace, this can never be a word
stopsentence = (".", "!", "?", "\n") # Cause a "new sentence" if found at the end of a word
sentencesep  = "\n" #String used to seperate sentences


# GENERATE TABLE
w1 = stopword
w2 = stopword
table = {}

with open("twts.txt") as file:
    for line in file:
        for word in line.split():
            if word[-1] in stopsentence:
                table.setdefault( (w1, w2), [] ).append(word[0:-1])
                w1, w2 = w2, word[0:-1]
                word = word[-1]
            table.setdefault( (w1, w2), [] ).append(word)
            w1, w2 = w2, word
# Mark the end of the file
table.setdefault( (w1, w2), [] ).append(stopword)
# GENERATE SENTENCE OUTPUT
maxsentences  = 3

w1 = stopword
w2 = stopword
sentencecount = 0
sentence = []

while sentencecount < maxsentences:
    newword = random.choice(table[(w1, w2)])
    if newword == stopword: sys.exit()
    if newword in stopsentence:
        print "%s%s%s" % (" ".join(sentence), newword, sentencesep)
        sentence = []
        sentencecount += 1
    else:
        sentence.append(newword)
    w1, w2 = w2, newword
