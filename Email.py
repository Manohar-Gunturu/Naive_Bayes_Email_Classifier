import re
class Email:
    def __init__(self,name,num):
        self.name = name
        self.vocabulary = dict()
        self.num = num
        self.num_emails = 0

    def readFile(self,fileName):
        with open(fileName, encoding ='latin-1') as file_handle:
            self.num_emails = self.num_emails + 1
            entries = file_handle.read()
            line2 = re.split('[^a-zA-Z]', entries)
            # print(
            for word in line2:
                if not word:
                    continue
                word = word.lower().strip()
                if(len(word) == 0):
                    continue

                if word not in self.vocabulary.keys():
                    self.vocabulary[word] = 1
                    self.num =  self.num + 1
                else:
                    self.vocabulary[word] = self.vocabulary[word] + 1
                    self.num = self.num + 1


    def decrement_num(self, word):
        self.num = self.num - self.vocabulary[word]

    def read_allFiles(self,categoty,filenameList):
        i = 0
        for fileName in filenameList:
            if fileName[6:9] == categoty:
                self.readFile("train/"+fileName)
                i = i + 1
        print(i)

