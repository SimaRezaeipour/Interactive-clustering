# -*- coding: utf-8 -*-

# import spacy
# nlp = spacy.load('en')
# doc = nlp(open("testFile").read().decode('utf8'))
#
# sentences = [sent.string.strip() for sent in doc.sents]
#
#
#
import spacy
from spacy import displacy

# text = u"""Darcy S.
# Darcy S. Best 41 Leblanc Avenue West Timmins, Ontario, Canada P4N 3J4 Cell:    1 (705) 262-1946 darc
# Mary Sent
# Mary Sent from my iPad   Hi Jason, I can get you in contact with Mark if you would like. Amy   Hi Am
# **************<br>
# Jason
# Jason, I can get you in contact with Mark if you would like. Amy   Hi Amy, Yes please!  Thanks, Jaso
# **************<br>
# Mark
# Mark if you would like. Amy   Hi Amy, Yes please!  Thanks, Jason """
#
# nlp = spacy.load('en_core_web_sm')
# doc = nlp(text)
# displacy.serve(doc, style='ent')


import os
nlp = spacy.load('en') # install 'en' model (python3 -m spacy download en)
# doc = nlp(u"""Are there any Respiratory Therapists in either an acute setting or
# community setting administrating  Naloxone for suspected opioid overdoses?
# Would you be willing to share any practice documents that you may have?
# Thanks,
#
# Andrea Wnuk, BSc, RRT, MHA
# Professional Practice Lead
# Respiratory Services, Vancouver Acute
# T: 604-875-4111 ext. 54896
# """)
# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)

#
# def getNERs():
#     locations = {}
#     userDirectory = "emailsClean"
#     dirFileList = os.listdir(userDirectory + "/emails")
#     dirFileList.sort()
#     index = 0
#     for file in dirFileList:
#         if file.endswith('.txt'):
#             documentFile = open(userDirectory + "/emails/" + file, 'r')
#             doc = documentFile.read()
#             documentFile.close()
#
#             doc = doc.replace('%' * 100, '').replace('\n', ' ').decode('utf8')
#             doc_nlp = nlp(doc)
#
#             for ent in doc_nlp.ents:
#                 if ent.label_ == "PERSON":
#                     print(ent.text)
#                     print(doc[ent.start_char: ent.end_char + 100].replace('\n', ' '))
#                     print("**************<br>")
#
# getNERs()


files = open('/home/ehsan/Desktop/app.csv', 'r')
index = 1

for line in files:
    temp = open( "/home/ehsan/Desktop/felwah/"+ str(index) + ".txt", 'w')
    temp.write(line)
    temp.close()
    index += 1

files.close()