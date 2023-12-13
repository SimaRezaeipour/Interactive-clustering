import string
import re
import unicodedata
from nltk.stem.wordnet import WordNetLemmatizer
import urllib
import sentenceSimilarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

def cleanText(text, onlyEnglish, numbers, lematizer):
    """
    prepare the clean text as following:
    1) remove stopwords
    2) remove punctuations
    3) lower case
    4) remove none english chars
    5) Remove new line, Tab and double spaces
    6) Remove numbers
    7) Lematizer (wordnet based)
    8) remove terms less than 2 chars in length
    :param text:
    :param onlyEnglish: if true none english alphabet will be replaced with english ones
    :param numbers: if ture numbers will be removed
    :return:
    """
    text = text.translate(string.maketrans(string.punctuation, ' ' * len(string.punctuation)))  # Remove Punctuations
    text = text.lower()  # Lower case
    if onlyEnglish == "yes":#remove none english chars
        text = re.sub(r'[^\a-z0-9]',' ', text)
    if numbers == "yes": # remove numbers
        text = re.sub(r'[0-9]' , "", text)
    text = re.sub('\s+', ' ', text).strip()  # Remove new line, Tab and double spaces
    if lematizer == "yes":#lematixer
        temp = ""
        for term in text.split(' '):
            temp += WordNetLemmatizer().lemmatize(term) + ' '
        text = re.sub('\s+', ' ', temp).strip()

    # remove terms less than 2 chars in length
    text = re.sub(r'\b.{2}\b', ' ', text).strip()
    # remove stopwords (it will be removed in count and tfidf vectorizor)
    # for sword in stopwords:
    #     text = re.sub(r'\b%s\b' % sword, "", text)  # word boundary
    text = re.sub('\s+', ' ', text).strip()  # Remove new line, Tab and double spaces
    text = unicode(text, errors='replace')
    return text

def searchMedilexicon(keyword, topK=2):
    results = []

    query = "http://www.medilexicon.com/abbreviations?search=" + keyword + "&target=abbreviations"
    searchResults = urllib.urlopen(query).read()

    pattern = re.compile(r'<strong class="item_text_normal">(.+?)<')

    counter = 0
    for matched in re.finditer(pattern, searchResults):
        results.append(re.sub('\(.*\)','', matched.group(1)).strip())
        counter += 1
        if counter >= topK:
            break

    return results

def getSentenceSimilarity(array, sentence):
    similarities = []
    for element in array:
        # similarities.append(sentenceSimilarity.semantic_similarity(element, sentence, False))
        similarities.append(sentenceCosineSimilarity(element, sentence))
    return similarities

def sentenceCosineSimilarity(sentence1, sentence2):
    corpus = []
    corpus.append(sentence1)
    corpus.append(sentence2)
    tf_vectorizer = CountVectorizer(ngram_range=(2, 3), min_df=1, analyzer='char', stop_words="english")
    tf = tf_vectorizer.fit_transform(corpus)
    return cosine_similarity(tf)[0, 1]


# print getSentenceSimilarity(searchMedilexicon("AIDS", 3), "Emergence of the Acquired Immunodeficiency Syndrome")

# print sentenceCosineSimilarity("Body Temperature and Pressure Saturated", "Ambient Pressure Saturated With Water Vapour Pressure")

