# -*- coding: utf-8 -*-

import csv
import re
from datetime import date
from datetime import datetime
from dateutil.parser import parse
import operator
import numpy as np
import os
import sys
import spacy
nlp = spacy.load('en')

subjects = {}
dates = {}
bodys = {}
senderNames = {}
senderEmail = {}
listnames = {}
attachNum = {}
subjectStat = {}
cleanBodys = {}
authorSignature = {}
authorSignatureEducation = {}

def readEmailCSV(fileAddress="", senderCol=3, subjectCol=0, dateCol=5,
                 bodyCol=2, listNameCol=1, senderEmailCol=4, attachCol=6):

    firstrow = True
    with open(fileAddress, 'rb') as csvfile:
        emailreader = csv.reader(csvfile, delimiter=',')
        for index, row in enumerate(emailreader):
            if firstrow:
                firstrow = False
            else:
                # get email subject
                subject = re.sub(r'(.*\]\s+)','', row[subjectCol])
                subject = re.sub(r'(.*FW:\s)', '', subject)
                subject = re.sub(r'(.*Fwd:\s)', '', subject)
                subject = re.sub(r'(.*RE:\s)', '', subject)

                if subject in subjects:
                    subjects[subject].append(index)
                else:
                    subjects[subject] = []
                    subjects[subject].append(index)

                #get email date
                # try:
                #     dates[index] = datetime.strptime(row[dateCol], "%a, %d %b %Y %H:%M:%S")
                # except:
                #     month, day, year = row[dateCol].split('/')
                #     dates[index] = date(int(year), int(month), int(day))
                dates[index] = parse(row[dateCol])

                #get email body
                bodys[index] = row[bodyCol]

                #get Sender Name
                senderNames[index] = row[senderCol]

                #get list name (sent to)
                listnames[index] = row[listNameCol]

                #get sender email
                senderEmail[index] = row[senderEmailCol]

                #get attachments number
                attachNum[index] = row[attachCol]

def separateEmails(dateThreshold=30):
    """
    ***** Important: assumed emails are sorted by date
    :param dateThreshold:
    :return:
    """

    subjectIndex = 0

    for subject in subjects:
        for count, index in enumerate(subjects[subject]):
            if count == 0:
                previousIndex = index
                fileName = str(dates[index].year) + "_" + \
                               str('%02d' % dates[index].month) + "_" + \
                               str('%02d' % dates[index].day) + "_" + \
                               re.sub(r'[^a-zA-Z0-9]', ' ', subject).replace("  "," ").strip()

                emailThreadContent = subject + "\n"
                emailThreadContent += str(dates[index]) + "\n"
                emailThreadContent += "\n" + 100 * "%" + "\n"
                emailThreadContent += getUsefulContent(bodys[index], index) + "\n"
                subjectStat["subject" + str(subjectIndex)] = 0
            else:
                if (dates[index] - dates[previousIndex]).days > dateThreshold:
                    #save previous email thread
                    writeFile = open("emailsClean/emails/" + fileName + '.txt', 'w')
                    writeFile.write(emailThreadContent)
                    writeFile.close()

                    fileName = str(dates[index].year) + "_" + \
                               str('%02d' % dates[index].month) + "_" + \
                               str('%02d' % dates[index].day) + "_" + \
                               re.sub(r'[^a-zA-Z0-9]', ' ', subject).replace("  "," ").strip()

                    emailThreadContent = subject + "\n"
                    emailThreadContent += str(dates[index]) + "\n\n"
                    emailThreadContent += "\n" + 100 * "%" + "\n"
                    emailThreadContent += getUsefulContent(bodys[index], index) + "\n"
                    subjectIndex += 1
                    subjectStat["subject" + str(subjectIndex)] = 0
                else:
                    emailThreadContent += "\n" + 100 * "%" + "\n"
                    emailThreadContent += getUsefulContent(bodys[index], index) + "\n"
                    subjectStat["subject" + str(subjectIndex)] += 1
                previousIndex = index

            # save email thread
            writeFile = open("emailsClean/emails/" + fileName + '.txt', 'w')
            writeFile.write(emailThreadContent)
            writeFile.close()
        subjectIndex += 1

def getUsefulContent(text, bodyIndex):
    """
    It is now rule based with string matching. More complicated formula is need to extend this method.
    :param text:
    :return:
    """

    if "-------" in text:
        index = text.index('-------')
        text = text[0:index]

    if "\nFrom: " in text:
        index = text.index('\nFrom: ')
        text = text[0:index]

    if "____________" in text:
        index = text.index('____________')
        text = text[0:index]

    if "\n********" in text:
        index = text.index('\n********')
        text = text[0:index]

    if "\nConfidentiality Statement" in text:
        index = text.index('\nConfidentiality Statement')
        text = text[0:index]

    if "\nThis information is directed in confidence" in text:
        index = text.index('\nThis information is directed in confidence')
        text = text[0:index]

    if "-----Original Message" in text:
        index = text.index('-----Original Message')
        text = text[0:index]

    pattern = re.compile(r'On(.*?)wrote:')
    for matched in re.finditer(pattern, text):
        text = text[0:matched.start()]
        break  # first one is enough

    if "\nQuoting " in text:
        index = text.index('\nQuoting ')
        text = text[0:index]

    # Handling confidentiality
    if "\nCONFIDENTIALITY NOTICE" in text:
        index = text.index('\nCONFIDENTIALITY NOTICE')
        text = text[0:index]

    if "\nCONFIDENTIALITY STATEMENT" in text:
        index = text.index('\nCONFIDENTIALITY STATEMENT')
        text = text[0:index]

    if "\nThe information contained in this" in text:
        index = text.index('\nThe information contained in this')
        text = text[0:index]

    if "\nThis electronic transmission is strictly confidential" in text:
        index = text.index('\nThis electronic transmission is strictly confidential')
        text = text[0:index]

    if "\nConfidentiality Notice:" in text:
        index = text.index('\nConfidentiality Notice:')
        text = text[0:index]

    if "\n*** This communication" in text:
        index = text.index('\n*** This communication')
        text = text[0:index]

    if "\nConfidentiality/Privacy Notice" in text:
        index = text.index('\nConfidentiality/Privacy Notice')
        text = text[0:index]

    if "\nThis e-mail and attachments are only" in text:
        index = text.index('\nThis e-mail and attachments are only')
        text = text[0:index]

    if "\nThis electronic message and any files" in text:
        index = text.index('\nThis electronic message and any files')
        text = text[0:index]

    if 'This information is directed in confidence solely' in text:
        index = text.index('This information is directed in confidence solely')
        text = text[0:index]

    if 'This message is intended only for the named' in text:
        index = text.index('This message is intended only for the named')
        text = text[0:index]

    if 'This e-mail message, including any attachments' in text:
        index = text.index('This e-mail message, including any attachments')
        text = text[0:index]

    if 'This email and any files transmitted' in text:
        index = text.index('This email and any files transmitted')
        text = text[0:index]

    if 'This communication is intended for the use of the recipient' in text:
        index = text.index('This communication is intended for the use of the recipient')
        text = text[0:index]

    if 'This message is intended for the person to whom' in text:
        index = text.index('This message is intended for the person to whom')
        text = text[0:index]

    if 'This email may contain confidential' in text:
        index = text.index('This email may contain confidential')
        text = text[0:index]

    if 'This e-mail may contain confidential' in text:
        index = text.index('This e-mail may contain confidential')
        text = text[0:index]

    if 'Confidentialité   | Confidentiality' in text:
        index = text.index()
        text = text[0:index]

    text = text.replace('Confidentialit� <http://www.jgh.ca/confidentialitecourriel>  | Confidentiality <http://www.jgh.ca/emailconfidentiality>','')
    text = text.replace('<http://www.jgh.ca/confidentialitecourriel> <http://www.jgh.ca/emailconfidentiality>', '')
    text = text.replace('<http://www.jgh.ca/>','')
    text = re.sub(r'(Confidentialité.*?\|\sConfidentiality)', '', text)

    #handeling html tags
    text = re.sub(r'<.*?>', '', text)

    #remove white spaces
    text = text.replace('\t', ' ')

    beforeLen = len(text)
    text = re.sub('[\r\n]{2,}', '\n', text)
    text = re.sub('\n\s\n', '\n', text)
    nowLen = len(text)
    while(beforeLen > nowLen):
        beforeLen = len(text)
        text = re.sub('[\r\n]{2,}', '\n', text)
        text = re.sub('\n\s\n', '\n', text)
        nowLen = len(text)

    text = text.strip()
    cleanBodys[bodyIndex] = text

    # remove signatures
    return removeSignature(bodyIndex, text)

def getStatistics():
    usersIndex = 0
    users = {}

    print("Number of emails: " + str(len(set(senderNames))))
    print("Number of subjects: " + str(len(subjects)))

    # number of users
    for nameIndedx in senderNames:
        if senderNames[nameIndedx] in users:
            users[senderNames[nameIndedx]] += 1
        else:
            users[senderNames[nameIndedx]] = 1
            usersIndex += 1
    print("Number of users: " + str(usersIndex))

    # top 10 active users
    sorted_users = sorted(users.items(), key=operator.itemgetter(1))
    print("Top 10 active users:")
    for i in range(1, 11):
        print("\t"+sorted_users[len(sorted_users) - i - 1][0] + ", " + str(sorted_users[len(sorted_users) - i - 1][1]))

    # email dates
    print("First email date: " + str(dates[1]))
    print("Last email date: " + str(dates[len(dates)]))

    # number of emails per month and year
    monthStatistics = {}
    yearStatistics = {}
    for dateIndex in dates:
        tempMonth = str(dates[dateIndex].month) + "/" + str(dates[dateIndex].year)
        if tempMonth in monthStatistics:
            monthStatistics[tempMonth] += 1
        else:
            monthStatistics[tempMonth] = 1

        tempYear = str(dates[dateIndex].year)
        if tempYear in yearStatistics:
            yearStatistics[tempYear] += 1
        else:
            yearStatistics[tempYear] = 1

    print("Number of emails per month:")
    for item in monthStatistics:
        print("\t" + item + ", " + str(monthStatistics[item]))

    print("Number of emails per year:")
    for item in yearStatistics:
        print("\t" + item + ", " + str(yearStatistics[item]))

    # average response per email subject
    responsesArray = np.zeros(len(subjectStat))
    for index, statIndex in enumerate(subjectStat):
        responsesArray[index] = subjectStat[statIndex]
    print("Average response per email subject: " +str(np.round(np.average(responsesArray), 2)))
    print("Maximum response for an email subject: " + str(np.max(responsesArray)))
    print("Minimum response for an email subject: " + str(np.min(responsesArray)))

    # emails per list statistics
    listStat = {}
    for listIndex in listnames:
        if listnames[listIndex] in listStat:
            listStat[listnames[listIndex]] +=1
        else:
            listStat[listnames[listIndex]] = 1
    print("Emails per list statistics:")
    for listName in listStat:
        print("\t" + listName + ": " + str(listStat[listName]))

def getNERs():
    locations = {}
    userDirectory = "emailsClean"
    dirFileList = os.listdir(userDirectory + "/emails")
    dirFileList.sort()
    index = 0
    for file in dirFileList:
        if file.endswith('.txt'):
            documentFile = open(userDirectory + "/emails/" + file, 'r')
            doc = documentFile.read()
            documentFile.close()

            doc = nlp(doc.replace('%' * 100, '').replace('\n', ' ').decode('utf8'))

            for ent in doc.ents:
                if ent.label_ == "GPE":
                    if ent.text in locations:
                        locations[ent.text] += 1
                    else:
                        locations[ent.text] = 1

    sorted_locations = sorted(locations.items(), key=operator.itemgetter(1))
    for i in range(0, len(sorted_locations)):
        print sorted_locations[len(sorted_locations) - i - 1]

def removeSignature(name_index, cleanText):
    if len(senderNames[name_index]) > 2:
        # create name combination
        namecombination = []
        namecombination.append(senderNames[name_index])
        namecombination.append(senderNames[name_index].lower())
        newName = re.sub(r'\(.*\)', '', senderNames[name_index]).strip()
        namecombination.append(newName)
        namecombination.append(newName.lower())

        if ', ' in newName:
            temp = newName.split(', ')
            if len(temp[1]) > 1:
                namecombination.append(temp[1])
                namecombination.append(temp[1].lower())
            if len(temp[0]) > 1:
                namecombination.append(temp[0])
                namecombination.append(temp[0].lower())
            namecombination.append(temp[1] + " " + temp[0])
            namecombination.append((temp[1] + " " + temp[0]).lower())
        else:
            temp = newName.split(' ')
            if len(temp[0]) > 1:
                namecombination.append(temp[0])
                namecombination.append(temp[0].lower())
            if len(temp[len(temp) - 1]) > 1:
                namecombination.append(temp[len(temp) - 1])
                namecombination.append((temp[len(temp) - 1]).lower())

        # print namecombination
        found = False
        found_index = sys.maxint
        for nameCob in namecombination:
            if nameCob in cleanText:
                if cleanText.rfind(nameCob) > 20:
                    if cleanText.rfind(nameCob) < found_index:
                        found_index = cleanText.index(nameCob)
                        found = True

        if found == True:
            # print cleanText.replace('\n', ' ')
            # print cleanText[0:cleanText.rfind(nameCob)].replace('\n', ' ')
            # return cleanText[0:cleanText.rfind(nameCob)]
            return cleanText[0:found_index]
    else:
        namecombination = ['Vanessa Roberts', 'Vanessa', 'vanessa roberts', 'vanessa']
        cleanText = cleanBodys[name_index]

        for nameCob in namecombination:
            if nameCob in cleanText:
                return cleanText[0:cleanText.index(nameCob)]
                break
    return cleanText

def getSignatures():
    count = 0

    for name_index in senderNames:
        if len(senderNames[name_index]) > 2:
            # create name combination
            namecombination = []
            namecombination.append(senderNames[name_index])
            namecombination.append(senderNames[name_index].lower())
            newName = re.sub(r'\(.*\)', '', senderNames[name_index]).strip()
            namecombination.append(newName)
            namecombination.append(newName.lower())

            if ', ' in newName:
                temp = newName.split(', ')
                if len(temp[1]) > 1:
                    namecombination.append(temp[1])
                    namecombination.append(temp[1].lower())
                if len(temp[0]) > 1:
                    namecombination.append(temp[0])
                    namecombination.append(temp[0].lower())
                namecombination.append(temp[1] + " " + temp[0])
                namecombination.append((temp[1] + " " + temp[0]).lower())
            else:
                temp = newName.split(' ')
                if len(temp[0]) > 1:
                    namecombination.append(temp[0])
                    namecombination.append(temp[0].lower())
                if len(temp[len(temp) - 1]) > 1:
                    namecombination.append(temp[len(temp) - 1])
                    namecombination.append((temp[len(temp) - 1]).lower())

            # print namecombination
            cleanText = cleanBodys[name_index]
            found = False
            found_index = sys.maxint
            for nameCob in namecombination:
                if nameCob in cleanText:
                    # print cleanText[cleanText.index(nameCob):cleanText.index(nameCob)+100].replace('\n', ' ')
                    if cleanText.rfind(nameCob) > 20:
                        if cleanText.rfind(nameCob) < found_index:
                            found_index = cleanText.index(nameCob)
                            found = True
            if found == True:
                # print cleanText[cleanText.rfind(nameCob):].replace('\n', ' ')
                # print "****" + senderNames[name_index]

                # print cleanText[found_index:].replace('\n', ' ') # better
                # print "****" + str(namecombination)
                if senderNames[name_index] in authorSignature:
                    if len(authorSignature[senderNames[name_index]]) < len(cleanText[found_index:].replace('\n', ' ')):
                        authorSignature[senderNames[name_index]] = cleanText[found_index:].replace('\n',' ')
                else:
                    authorSignature[senderNames[name_index]] = cleanText[found_index:].replace('\n', ' ')

                count += 1

            # if found == False:
                # print namecombination
                # print cleanText.replace('\n', ' ') + "\n"
        else:
            namecombination = ['Vanessa Roberts', 'Vanessa', 'vanessa roberts', 'vanessa']
            cleanText = cleanBodys[name_index]

            for nameCob in namecombination:
                if nameCob in cleanText:
                    # print cleanText[:cleanText.index(nameCob):].replace('\n', ' ')
                    count += 1
                    break
            # print "****" + senderEmail[name_index]
            # print cleanBodys[name_index].replace('\n', ' ') + "\n"

    print(count)

# readEmailCSV(fileAddress="Resources/emails(sorted).csv", senderCol=0, subjectCol=1, dateCol=2, bodyCol=5)
readEmailCSV(fileAddress="Resources/CSRT - Listserv.csv")
separateEmails(dateThreshold=30)
getSignatures()
# getStatistics()
# getNERs()

degreeNames = ['RT',
               'CRT',
               'BRT',
               'MHA',
               'B.Sc',
               'BSc',
               'RRT',
               'RN',
               'AA',
               'FCSRT',
               'MD',
               'CRE',
               'CAE',
               'Registered Respiratory Therapist',
               'Respiratory Therapist',
               'Anesthesia Assistant',
               'Fellow of the Canadian Society for Respiratory Therapists',
               'Medical Doctor',
               'Fellow of the Royal College of Physicians of Canada',
               'Certified Respiratory Educator',
               'Certified Asthma Educator',
               'R.R.T.',
               'M.Ed',
               'Charge Respiratory Therapist']
for author in authorSignature:
    authorSignatureEducation[author] = ""
    for dn in degreeNames:
        if dn in authorSignature[author]:
            authorSignatureEducation[author] += dn + ", "


for author in authorSignatureEducation:
    print(author + "\t" + authorSignatureEducation[author])