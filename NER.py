import csv
import re
import utility
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tokenize import sent_tokenize
from nltk.tag import StanfordNERTagger

firstrow = True
emailDate = []
emailSubject = []
listName = []
emailContent = []
threadContent = {}
threadDate = []
names = []
st = StanfordNERTagger('/home/ehsan/Documents/stanford-ner-2017-06-09/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '/home/ehsan/Documents/stanford-ner-2017-06-09/stanford-ner.jar')

location_hash = {}
organization_hash = {}
person_name_hash = {}

with open('Resources/emails (all).csv', 'rb') as csvfile:
    emailreader = csv.reader(csvfile, delimiter=',')
    for index, row in enumerate(emailreader):
        # print row.replace('\r','').replace('\n','')
        if firstrow:
            firstrow = False
        else:
            names.append(row[0])
            emailDate.append(re.sub(r'(.*/)','', row[2]))
            emailSubject.append(re.sub(r'(.*\]\s+)','', row[1]))
            emailContent.append(utility.cleanText(row[5], 'yes', 'yes', 'no'))
            sentences = sent_tokenize(row[5].decode('utf-8', 'ignore'))
            # for sent in sentences:
            #     print sent
            # print sentences[0]
            # print ne_chunk(pos_tag(word_tokenize(sentences[0].decode('utf-8', 'ignore'))))
            # print "*********************** Processing email thread " + str(index)
            for sentence in sentences:
                print "S> " +sentence
                # stanford_ner = st.tag(word_tokenize(sentence.decode('utf-8', 'ignore')))
                # previous_tag = ""
                # word = ""
                # for ner in stanford_ner:
                #     if ner[1] == "ORGANIZATION":
                #         if previous_tag == "ORGANIZATION":
                #             word += " " + ner[0]
                #         else:
                #             previous_tag =  "ORGANIZATION"
                #             word = ner[0]
                #     if ner[1] == "LOCATION":
                #         if previous_tag == "LOCATION":
                #             word += " " + ner[0]
                #         else:
                #             previous_tag = "LOCATION"
                #             word = ner[0]
                #     if ner[1] == "PERSON":
                #         if previous_tag == "PERSON":
                #             word += " " + ner[0]
                #         else:
                #             previous_tag = "PERSON"
                #             word = ner[0]
                #     else:
                #         if previous_tag == "LOCATION":
                #             if word != "":
                #                 print "LOCATION " + word
                #             word = ""
                #         if previous_tag == "ORGANIZATION":
                #             if word != "":
                #                 print "ORGANIZATION " + word
                #             word = ""
                #         if previous_tag == "PERSON":
                #             if word != "":
                #                 print "PERSON " + word
                #             word = ""
                #         previous_tag = ner[1]
            # listName.append(row[6])


# listNameHash = {}
# for data in listName:
#     if data in listNameHash:
#         listNameHash[data] = listNameHash[data] + 1
#     else:
#         listNameHash[data] = 1
#
#
# print str(len(set(names)))
#
# print "statistics:"
# print "# Emails: " + str(len(emailContent))
# print "# Emails threads: " + str(len(set(emailSubject)))
#
# for item in listNameHash:
#     print str(item) + "\t" + str(listNameHash[item])
#
# for index, subject in enumerate(emailSubject):
#     if subject in threadContent:
#         threadContent[subject] = threadContent[subject] + ' ' + emailContent[index]
#     else:
#         threadContent[subject] = emailContent[index]
#         threadDate.append(emailDate[index])
#
# # #save emails
# # for index, email in enumerate(emailContent):
# #     writeFile = open('emails/email'+str(index+1)+'_'+str(emailDate[index]) +'.txt','w')
# #     writeFile.write(email)
# #     writeFile.close()
#
# #save threads
# for index, subject in enumerate(threadContent):
#     writeFile = open('emails/'+str(threadDate[index])+'_email'+str(index+1)+'.txt','w')
#     writeFile.write(threadContent[subject])
#     writeFile.close()