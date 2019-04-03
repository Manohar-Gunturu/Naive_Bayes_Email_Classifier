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
print("Performance", performance)


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
freq_list = [1, 5, 10, 15, 20]

for freq in freq_list:
    print("-------------- freq ",  str(freq)  , " ----------------------")
    freq_ham = copy.deepcopy(ham)
    freq_spam = copy.deepcopy(spam)
    for word in list(freq_ham.vocabulary.keys()):
        if freq_ham.vocabulary[word] <= freq:
            freq_ham.decrement_num(word)
            del freq_ham.vocabulary[word]

    for word in list(freq_spam.vocabulary.keys()):
        if freq_spam.vocabulary[word] <= freq:
            freq_spam.decrement_num(word)
            del freq_spam.vocabulary[word]

    print("Ham vocabulary size ", len(freq_ham.vocabulary))
    print("spam vocabulary size ", len(freq_spam.vocabulary))
    Vocabulary3 = model_builder.build(freq_ham, freq_spam)
    model_builder.Printer(Vocabulary3, "freq"+str(freq)+"-model.txt")
    performance = model_builder.classify(testList, Vocabulary3, "freq"+str(freq)+"-result.txt")
    print("     Performance", performance)


print("----------------- exp 4b -----------------")
#top 5% is calculated in following way
#sort them based on frequencies and remove top 5% words











