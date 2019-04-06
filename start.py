import os,copy
import Email
import model_builder

filePath = 'train'
filenameList = os.listdir(filePath)
# add 0.5 smooth


ham = Email.Email("ham",  0)
spam = Email.Email("spam", 0)
ham.read_allFiles("ham", filenameList)
spam.read_allFiles("spa", filenameList)
print("Ham vocabulary size " , len(ham.vocabulary))
print("spam vocabulary size ", len(spam.vocabulary))
model_builder.build_scores(ham, spam)
Vocabulary1 = model_builder.build(ham,spam)
model_builder.Printer(Vocabulary1, "model.txt")
testList = os.listdir("test")
performance = model_builder.classify(testList, Vocabulary1, "baseline-result.txt")
print("Performance", performance)


# section 1.3.1 stop words
ham_stop_words = copy.deepcopy(ham)
spam_stop_words = copy.deepcopy(spam)

with open("English-Stop-Words.txt", encoding ='latin-1') as file_handle:
    entries = file_handle.readlines()
    for line in entries:
        line = line.strip()
        if line in ham_stop_words.vocabulary.keys():
            ham_stop_words.decrement_num(line)
            del ham_stop_words.vocabulary[line]
        if line in spam_stop_words.vocabulary.keys():
            spam_stop_words.decrement_num(line)
            del spam_stop_words.vocabulary[line]

print("----- StopWords Removal--------")
print("Ham vocabulary size " , len(ham_stop_words.vocabulary))
print("spam vocabulary size ", len(spam_stop_words.vocabulary))
Vocabulary2 = model_builder.build(ham_stop_words,spam_stop_words)
model_builder.Printer(Vocabulary2,"stopword-model.txt")
performance = model_builder.classify(testList, Vocabulary2,"stopword-result.txt")
print("Accuracy", performance)


ham_size_words = copy.deepcopy(ham)
spam_size_words = copy.deepcopy(spam)
print("---Removing words length <= 2 and length >= 9----")
for word in list(ham_size_words.vocabulary.keys()):
    if len(word) <= 2 or len(word) >= 9:
        ham_size_words.decrement_num(word)
        del ham_size_words.vocabulary[word]

for word in list(spam_size_words.vocabulary.keys()):
    if len(word) <= 2 or len(word) >= 9:
        spam_size_words.decrement_num(word)
        del spam_size_words.vocabulary[word]

print("Ham vocabulary size " , len(ham_size_words.vocabulary))
print("spam vocabulary size ", len(spam_size_words.vocabulary))
Vocabulary3 = model_builder.build(ham_size_words,spam_size_words)
model_builder.Printer(Vocabulary3,"wordlength-model.txt")
performance = model_builder.classify(testList, Vocabulary3,"wordlength-result.txt")
print("Performance", performance)


print("----------------- exp 4 --------------")
tj = input("enter limit to infrequent words")
#freq_list = [1, 5, 10, 15, 20]
freq_list = [int(tj)]
main_vocabulary = dict()
for freq in freq_list:
    print("-------------- freq ",  str(freq)  , " ----------------------")
    freq_ham = copy.deepcopy(ham)
    freq_spam = copy.deepcopy(spam)
    for word in list(freq_ham.vocabulary.keys()):
        x = freq_spam.vocabulary[word] if word in freq_spam.vocabulary.keys() else 0
        main_vocabulary[word] = freq_ham.vocabulary[word] +  x
        if freq_ham.vocabulary[word] +  x  <= freq:
            freq_ham.decrement_num(word)
            del freq_ham.vocabulary[word]

    for word in list(freq_spam.vocabulary.keys()):
        x = freq_ham.vocabulary[word] if word in freq_ham.vocabulary.keys() else 0
        main_vocabulary[word] = freq_spam.vocabulary[word] + x
        if freq_spam.vocabulary[word] + x <= freq:
            freq_spam.decrement_num(word)
            del freq_spam.vocabulary[word]

    print("Ham vocabulary size ", len(freq_ham.vocabulary))
    print("spam vocabulary size ", len(freq_spam.vocabulary))
    Vocabulary3 = model_builder.build(freq_ham, freq_spam)
    model_builder.Printer(Vocabulary3, "infreq"+str(freq)+"-model.txt")
    performance = model_builder.classify(testList, Vocabulary3, "infreq"+str(freq)+"-result.txt")
    print("   Accuracy", performance)


print("----------------- exp 4b -----------------")
#top 5% is calculated in following way
#sort them based on frequencies and remove top 5% words
print(len(main_vocabulary))
main_vocabulary = sorted(main_vocabulary.items(), key=lambda x: x[1], reverse=True)
v_size = len(main_vocabulary)

print("give 5% as 0.05, 10% as 0.10")
tj = input("enter limit to frequency words in %")
freq_list = [round(v_size*float(tj))]
#freq_list = [  round(v_size*0.05), round(v_size*0.10), round(v_size*0.15), round(v_size*0.20), round(v_size*0.25)  ]

for freq in freq_list:
    voacb_removal = main_vocabulary[ 0: freq - 1 ]
    ham_stop_words = copy.deepcopy(ham)
    spam_stop_words = copy.deepcopy(spam)
    for line in voacb_removal:
        line = line[0].strip()
        if line in ham_stop_words.vocabulary.keys():
            ham_stop_words.decrement_num(line)
            del ham_stop_words.vocabulary[line]
        if line in spam_stop_words.vocabulary.keys():
            spam_stop_words.decrement_num(line)
            del spam_stop_words.vocabulary[line]

    print("Ham vocabulary size ", len(ham_stop_words.vocabulary))
    print("spam vocabulary size ", len(spam_stop_words.vocabulary))
    Vocabulary2 = model_builder.build(ham_stop_words, spam_stop_words)
    model_builder.Printer(Vocabulary2, "freq-perc-model.txt")
    performance = model_builder.classify(testList, Vocabulary2, "freq-perc-result.txt")
    print("Accuracy", performance)










