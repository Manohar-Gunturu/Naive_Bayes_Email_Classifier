import solo_writer
import math, re


def smoothFrequemcy(email, key, numWord, flag):
    if (flag == True):
        result = (email.vocabulary[key] + 0.5) / (email.num + numWord * 0.5)
    else:
        result = 0.5 / (email.num + numWord * 0.5)
    return result


def Printer(Vocabulary, filename):
    with open(filename, 'w') as file_handle:
        i = 1
        for key in sorted(Vocabulary):
            list = Vocabulary[key]
            file_handle.write(
                str(i) + "  " + key + "  " + list[0] + "  " + str(list[1]) + "  " + list[2] + "  " + str(list[3]) + '\n')
            i = i + 1


def build(ham, spam):
    Vocabulary = {**ham.vocabulary, **spam.vocabulary}
    hamVocabulary = ham.vocabulary
    spamVocabulary = spam.vocabulary
    for key in Vocabulary.keys():
        if (key in hamVocabulary.keys()) & (key in spamVocabulary.keys()):
            Vocabulary[key] = [str(hamVocabulary[key]), smoothFrequemcy(ham, key, ham.num, True), str(spamVocabulary[key]),
                               smoothFrequemcy(spam, key, spam.num, True)]
        elif (key in hamVocabulary.keys()) & (key not in spamVocabulary.keys()):
            Vocabulary[key] = [str(hamVocabulary[key]), smoothFrequemcy(ham, key, ham.num, True), '0.5',
                               smoothFrequemcy(spam, key, spam.num, False)]
        else:
            Vocabulary[key] = ['0.5', smoothFrequemcy(ham, key, ham.num, False), str(spamVocabulary[key]),
                               smoothFrequemcy(spam, key, spam.num, True)]

    return Vocabulary



score_of_ham = 0
score_of_spam = 0

def build_scores(ham, spam):
    global score_of_spam,score_of_ham
    score_of_ham = math.log2(ham.num_emails / (ham.num_emails + spam.num_emails))
    score_of_spam = math.log2(spam.num_emails / (ham.num_emails + spam.num_emails))


def calc_score(fileName, Vocabulary):
    ham_tmp = score_of_ham
    spam_tmp = score_of_spam
    with open(fileName, encoding='latin-1') as file_handle:
        entries = file_handle.read()
        line2 = re.split('[^a-zA-Z]', entries)
        for word in line2:
            word = word.lower().strip()
            if word in Vocabulary.keys():
                ham_tmp += math.log2(Vocabulary[word][1])
                spam_tmp += math.log2(Vocabulary[word][3])
            else:
                pass

    return ham_tmp, spam_tmp


def classify(filenameList, Vocabulary, writeFile):
    solo_writer.open_trace(writeFile)
    performance = 0
    decision_helper = lambda a, b: 'right' if a == b else 'wrong'
    category_helper = lambda a: 'ham' if a[5:8] == 'ham' else 'spam'
    for fileName in filenameList:
        category = category_helper(fileName)
        ham_score, spam_score = calc_score("test/"+fileName, Vocabulary)
        if ham_score > spam_score:
            decision = decision_helper(category, "ham")
            if decision=='wrong':performance=performance + 1
            solo_writer.write(fileName + "  ham  "+str(ham_score)+"  "+str(spam_score)+ "  "+ category+"  "+ decision )
        else:
            decision = decision_helper(category, "spam")
            if decision == 'wrong': performance = performance + 1
            solo_writer.write(fileName + "  spam  " + str(ham_score) + "  " + str(spam_score)+ "  " + category +"  "+ decision)

    print("total ",len(filenameList)," wrong classified", performance)
    return (len(filenameList)-performance)/len(filenameList)




