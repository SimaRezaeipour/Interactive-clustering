#!/usr/bin/python
# Author: Ehsan Sherkat - 2016
import os
import re
import unicodedata
import string
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from time import time
import collections
import cgi, cgitb
import json
import utility
from sklearn.manifold import TSNE
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from scipy.sparse import coo_matrix
from sets import Set
from scipy.sparse import csr_matrix
import bhtsne
from nltk.tokenize import sent_tokenize

import spacy
nlp = spacy.load('en') # takes time to load


userDirectory = "emailsClean"
userID = "csrt3"
onlyEnglish = "yes" # if true, none english characters will be replaced with english one
numbers = "no" # if true numbers will be removed
lematizer = "no" # if true the text will be lemmatized based on wordnet
bigram = "no" # if true, bigrams and unigrams will be in term document matrix
perplexityNew = 18

ngram = 10
if bigram == "yes":
    ngram = 2

dirFileList = os.listdir(userDirectory + "/emails")
dirFileList.sort()
fileList = list() # list of files (the order is also used for document-term matrix)
stopwords = list()
allWords = {}
corpus = list() # the clean text of documents. Each documents is in a single line

# read resources
abrvExtension = {}
glossary = {}
indexDic = {}
vocabulary = []

def expandAbbreviations(text):
    terms = set(text.split(' '))
    for term in terms:
        if term in abrvExtension:
            text = re.sub(r'\b%s\b' % term, term + " " + abrvExtension[term], text)
    return text


 #read abbreviations
avrFile = open('Resources/extracted/abbreviation (all)')
for line in avrFile:
    line = line.replace('\n', '').replace('\r', '')
    parts = line.split('@')

    # get index of freqencies
    indexes = np.zeros((len(parts) - 1)/2)
    for i in range(0, (len(parts) - 1)/2):
        # print parts[2 * i + 2]
        indexes[i] = parts[2 * i + 2]

    abrvExtension[parts[0]] = parts[2 * np.argmax(indexes) + 1] # max freq disambiguation

    # add to vocabulary
    vocabulary.append(parts[0].lower())
    vocabulary.append(parts[2 * np.argmax(indexes) + 1].lower())


# read indexes
indexFile = open('Resources/extracted/index')
for line in indexFile:
    line = line.replace('\n', '').replace('\r', '')
    indexDic[line] = 1
    vocabulary.append(line)

# read glossary
glossaryFile = open('Resources/extracted/glossary')
for line in glossaryFile:
    line = line.replace('\n', '').replace('\r', '')
    glossary[line] = 1

    # add to vocabulary
    line = line.translate(string.maketrans(string.punctuation, ' ' * len(string.punctuation)))  # Remove Punctuations
    line = line.lower()
    vocabulary.append(line)

# create corpus
for file in dirFileList:
    if file.endswith('.txt'):
        documentFile = open(userDirectory + '/emails/' + file, 'r')
        documentText = ""
        for line in documentFile:
            # expand abbreviations
            expandAbbreviations(line)

            documentText += " " + utility.cleanText(line, onlyEnglish, numbers, lematizer)
        documentText = re.sub('\s+', ' ', documentText).strip()  # Remove new line, Tab and double spaces
        # check the size of file
        if documentText != "":
            fileList.append(file)
            corpus.append(documentText)


tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, ngram), min_df=1, vocabulary=set(vocabulary))
tfidf = tfidf_vectorizer.fit_transform(corpus)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# remove words that appeared in no document
newVocabulary = []
for column in np.nonzero(tfidf.sum(axis=0)[0])[1]:
    newVocabulary.append(tfidf_feature_names[column])

tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, ngram), min_df=1, vocabulary=set(newVocabulary))
tfidf = tfidf_vectorizer.fit_transform(corpus)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
tfidf_feature_names_hashmap = {}

# tfidf feature names hashmap
for i in range(0, len(tfidf_feature_names)):
    tfidf_feature_names_hashmap[tfidf_feature_names[i]] = i

for word in tfidf_feature_names:
    allWords[word] = 0

allWordsSorted = collections.OrderedDict(sorted(allWords.items()))

# create document term matrix (out) - tf-idf
document_term_matrix = ""
for i in range(0, len(fileList)):
    line = ""
    tfidf_hashmap = {}
    for col in tfidf.getrow(i).nonzero()[1]:
        if tfidf_feature_names[col] in allWordsSorted:
            tfidf_hashmap[col] = tfidf[i, col]

    for word, score in allWordsSorted.iteritems():
        word_index = tfidf_feature_names_hashmap.get(word)
        if tfidf_feature_names_hashmap.get(word) in tfidf_hashmap:
            line += str(tfidf_hashmap.get(word_index)) + ","
        else:
            line += "0.0,"
    line = line[0:line.rindex(',')]
    document_term_matrix += line + '\n'

# write document term matrix to file
document_term_matrix_file = open(userDirectory + "/process/out" + userID + ".Matrix", 'w')
document_term_matrix_file.write(document_term_matrix)
document_term_matrix_file.close()

# write all words
allwords_file = open(userDirectory + "/process/out" + userID + ".Terms", 'w')
for word, score in allWordsSorted.iteritems():
    allwords_file.write(word.encode('utf-8') + '\n')
allwords_file.close()

# write file list
fileList_file = open(userDirectory + "/process/fileList", 'w')
for fileName in fileList:
    fileList_file.write(unicode(fileName, errors='ignore') + '\n')
fileList_file.close()

# write spec file (reomve it later)
spec_file = open(userDirectory + "/process/out" + userID + ".Spec", 'w')
spec_file.write(str(len(fileList))+'\n')
spec_file.write(str(len(allWordsSorted))+'\n')
spec_file.close()

# run tsne
tsneFile = userDirectory + "/process/tsne"
os.system("cat "+ userDirectory + "/process/out" + userID + ".Matrix | tr ',' '\t' | ./bhtsne.py -d 2 -p "+str(perplexityNew)+" -o "+ tsneFile)

def getFontSize(rank):
    fontSize = "1"

    if rank >= 6:
        return "7"
    elif rank >= 4 and rank < 6:
        return "6"
    elif rank >= 2 and rank < 4:
        return "5"
    elif rank >= 1 and rank < 2:
        return "4"
    elif rank >= 0.5 and rank < 1:
        return "3"
    elif rank >= 0.2 and rank < 0.5:
        return "2"

    return fontSize

# extractive summary (ranked sentences) - Sentence Cloud
index = 0
for file in dirFileList:
    if file.endswith('.txt'):
        documentFile = open(userDirectory + "/emails/" + file, 'r')
        doc = documentFile.read()
        documentFile.close()

        # sentences = sent_tokenize(doc.replace('%'*100,'. '+'%'*100+'. ').decode('utf-8', 'ignore')) # for NLTK
        sentences = [sent.string.strip() for sent in nlp(doc.replace('%'*100,'. '+'%'*100+'. ').decode('utf8')).sents] # for spacy

        sentences_corpus = []
        for sentence in sentences:
            sentence = sentence.lower()
            # remove punctuations
            sentence = re.sub(r'\b.{2}\b', ' ', sentence).strip()
            sentence = re.sub(r'[!"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]', ' ', sentence).strip()
            sentences_corpus.append(sentence)

        count_vectorizer = CountVectorizer(ngram_range=(1, ngram), min_df=1, vocabulary=set(newVocabulary))
        countVector = count_vectorizer.fit_transform(sentences_corpus)

        sentence_rank_all = {}

        newDoc = ""

        for i in range(0, countVector.shape[0]):
            sentence_rank = 0.0
            cx = coo_matrix(countVector[i])
            for j, v in zip(cx.col, cx.data):
                sentence_rank += tfidf[index, j] * v
            sentence_rank_all[i] = sentence_rank
            newDoc += "<font size='" + getFontSize(sentence_rank) + "'>" + sentences[i] + "</font><br><br>"
        index += 1

        newDoc = "<font size='"+ str(1) +"'>"+newDoc+"</font>"

        # save email
        writeFile = open("emailsClean/process/sentenceCloud/" + file, 'w')
        writeFile.write(newDoc.encode('utf-8'))
        writeFile.close()