from itertools import permutations
import enchant
import csv 
import os

wordsFilePath = os.path.join('csv','words.csv')
nonWordsFilePath = os.path.join('csv','non_words.csv')

fields = ['S.NO','Word']
inp = 'EARIOTNSLCUDPMHGBFYWKVXZJQEARIOTNSLCUDPMHGBFY'
ls = enchant.list_languages()
wordList = []
nonWordList = []

#'en_BW', 'en_AU', 'en_BZ', 'en_GB', 'en_JM', 'en_DK', 'en_HK', 'en_GH', 'en_US', 'en_ZA', '
# en_ZW', 'en_SG', 'en_NZ', 'en_BS', 
# 'en_AG', 'en_PH', 'en_IE', 'en_NA', 'en_TT', 'en_IN', 'en_NG', 'en_CA']
BW = enchant.Dict("en_BW")
AU = enchant.Dict("en_AU")
BZ = enchant.Dict("en_BZ")
GB = enchant.Dict("en_GB")
JM = enchant.Dict("en_JM")
DK = enchant.Dict("en_DK")
HK = enchant.Dict("en_HK")
GH = enchant.Dict("en_GH")
US = enchant.Dict("en_US")
ZA = enchant.Dict("en_ZA")
ZW = enchant.Dict("en_ZW")
SG = enchant.Dict("en_SG")
NZ = enchant.Dict("en_NZ")
BS = enchant.Dict("en_BS")
AG = enchant.Dict("en_AG")
PH = enchant.Dict("en_PH")
IE = enchant.Dict("en_IE")
NA = enchant.Dict("en_NA")
TT = enchant.Dict("en_TT")
IN = enchant.Dict("en_IN")
NG = enchant.Dict("en_NG")
CA = enchant.Dict("en_CA")

def writeToCsv(filePath, word):
    f = open(filePath,'a')
    writer = csv.writer(f)
    data = ['0',word]
    writer.writerow(data)
    f.close

lettr = [x for x in inp]
for y in list(permutations(lettr, 5)):
    word="".join(y)
    if len(word)==5:

        if BW.check(word) or AU.check(word) or BZ.check(word) or GB.check(word) or JM.check(word) or DK.check(word) or HK.check(word) or GH.check(word)or US.check(word) or ZA.check(word) or ZW.check(word) or SG.check(word)or NZ.check(word) or BS.check(word) or AG.check(word) or PH.check(word)or IE.check(word) or NA.check(word) or TT.check(word) or NG.check(word)  or CA.check(word):
            if word not in wordList:
                writeToCsv(wordsFilePath,word) 
                wordList.append(word)
        else:
            if word not in nonWordList and word not in wordList:
                writeToCsv(nonWordsFilePath,word) 
                nonWordList.append(word)
        print(word)

