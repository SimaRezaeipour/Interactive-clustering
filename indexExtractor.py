import re
import utility
from nltk.corpus import stopwords

# bookIndex = open("Resources/eganIndex").read()
bookIndex = open("Resources/indexAll").read()

bookIndexWords = utility.cleanText(bookIndex, 'yes', 'yes', 'no').split(' ')

bookIndexWords = [word for word in bookIndexWords if word not in stopwords.words('english')] #remove stopwords

for word in bookIndexWords:
    print word

