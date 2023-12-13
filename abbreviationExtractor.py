import re
from nltk.corpus import stopwords
from wordsegment import load, segment
import utility
import numpy as np

stop_words = set(stopwords.words('english'))
load()

# data = open("Resources/FundamentalsRC").read()
data = open("Resources/allBooks").read()
# data = open("Resources/textbookRT").read()
# data = "fellow of the american association for respiratory care (FAARC)"

pattern = re.compile(r'(\([A-Z]{2,}\))')
abrvExtension = {}
abrvExtensionFreq = {}
i = 0

for matched in re.finditer(pattern, data):
    startIndex = matched.start()
    matchABR = matched.group()
    wordCount = 0
    size = len(matchABR) - 2
    index = 1
    abbreviation = ""

    try:
        tailSentence = segment(
            re.sub(r'[0-9]', '', data[startIndex - 150: startIndex].replace('-', '')))  # startIndex - 100
        allTrue = True
        while wordCount < size:
            wordNow = tailSentence[len(tailSentence) - index]

            if wordNow not in stop_words:
                wordCount += 1

                if wordNow[0] != matchABR[size - wordCount + 1].lower():
                    allTrue = False

                abbreviation = wordNow.capitalize() + " " + abbreviation
            else:
                abbreviation = wordNow + " " + abbreviation
            index += 1

        # print(abbreviation + matchABR)

        if not allTrue:
            candidates = utility.searchMedilexicon(matchABR[1:len(matchABR) - 1], topK=2)
            similarities = utility.getSentenceSimilarity(candidates, abbreviation)
            if len(similarities) > 0:
                bestIndex = np.array(similarities).argmax()
                if similarities[bestIndex] > 0.55:
                    currentABV = matchABR.replace('(', '').replace(')', '')
                    if currentABV not in abrvExtension:
                        abrvExtension[currentABV] = []
                        abrvExtension[currentABV].append(candidates[bestIndex].strip())
                        abrvExtensionFreq[candidates[bestIndex].strip()] = 1
                    else:
                        found = False
                        for item in abrvExtension[currentABV]:
                            if utility.sentenceCosineSimilarity(item, candidates[bestIndex].strip()) > 0.60:
                                abrvExtensionFreq[item] += 1
                                found = True
                                break

                        if found == False:
                            abrvExtension[currentABV].append(candidates[bestIndex].strip())
                            abrvExtensionFreq[candidates[bestIndex].strip()] = 1
                            print "1 => " + candidates[bestIndex]
                            print "2 => " + abrvExtension[currentABV][0] + "\n"
        else:
            currentABV = matchABR.replace('(', '').replace(')', '')
            if currentABV not in abrvExtension:
                abrvExtension[currentABV] = []
                abrvExtension[currentABV].append(abbreviation.strip())
                abrvExtensionFreq[abbreviation.strip()] = 1
            else:
                found = False
                for item in abrvExtension[currentABV]:
                    if utility.sentenceCosineSimilarity(item, abbreviation.strip()) > 0.60:
                        abrvExtensionFreq[item] += 1
                        found = True
                        break

                if found == False:
                    abrvExtension[currentABV].append(abbreviation.strip())
                    abrvExtensionFreq[abbreviation.strip()] = 1
                    print "1 => " + abbreviation
                    print "2 => " + abrvExtension[currentABV][0] + "\n"

        # i += 1
        # if i > 20:
        #     break

    except:
        print matchABR
        print tailSentence

for key, value in abrvExtension.items():
    tempLine = ""
    tempLine += key
    for item in value:
        tempLine += "@" + item + "@" + str(abrvExtensionFreq[item])
    print tempLine
