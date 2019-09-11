from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re

class wordProcessor:

    def clean_meaning(self, meaning):
        # Function to convert a raw review to a string of words
        # The input is a single string (a raw movie review), and
        # the output is a single string (a preprocessed movie review)
        #
        # 1. Remove HTML
        review_text = BeautifulSoup(meaning, "html.parser").get_text()
        #
        # 2. Remove non-letters
        letters_only = re.sub("[^a-zA-Z]", " ", review_text)
        #
        # 3. Convert to lower case, split into individual words
        words = letters_only.lower().split()
        #
        # 4. In Python, searching a set is much faster than searching
        #   a list, so convert the stop words to a set
        stops = set(stopwords.words("english"))
        #
        # 5. Remove stop words
        meaningful_words = [w for w in words if not w in stops]
        #
        # 6. Join the words back into one string separated by space,
        # and return the result.
        return (" ".join(meaningful_words))

    def sentence_to_wordslist(self, sentence, remove_stopwords=False):
        re.sub("[^a-zA-Z]", " ", sentence)
        words = sentence.lower().split()

        if remove_stopwords:
            stops = set(stopwords.words('english'))
            words = [w for w in words if w not in stops]

        return words