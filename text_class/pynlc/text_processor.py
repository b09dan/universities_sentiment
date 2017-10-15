from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy
from .corrector import correct, prepare_dictionary


class TextProcessor(object):
    def __init__(self, language, stopwords_whitelist, word2vec):
        """
        Initialize text processor
        :param language: language name (for nltk)
        :type language: str
        :param stopwords_whitelist: not remove stopword if it's part of these combinations (e.g. ["turn", "on"], ["turn", "off"])
        :type stopwords_whitelist: list[list[str]]
        :param word2vec: word2vec model
        :type word2vec: Word2Vec
        """
        self.language = language
        self.word2vec = word2vec
        self.stopwords = stopwords.words(language)
        self.stopwords_whitelist = stopwords_whitelist
        self.correction = True
        self.correction_dictionary = prepare_dictionary(self.word2vec.vocab)

    def corrected(self, word):
        """
        Get corrected word if can
        :param word: word
        :type word: str
        :return: word or None
        :rtype: str|NoneType
        """
        if not self.correction:
            if word in self.word2vec.vocab:
                return word
            else:
                return None
        else:
            return correct(word, self.correction_dictionary)

    def split(self, text):
        """
        Split text
        :param text: text
        :type text: str
        :return: splitted text
        :rtype: list[str]
        """
        words = word_tokenize(text.lower(), self.language)
        corrected_words = [self.corrected(word) for word in words
                           if word.isalnum() and word is not None]
        not_none_words = [word for word in corrected_words
                          if word is not None]
        result = []
        for word in not_none_words:
            if word not in self.stopwords:  # if word isn't stopword - store it
                result.append(word)
            else:  # for stopword - check "whitelisting"
                for stopwords_whitelist_combination in self.stopwords_whitelist:
                    if word not in stopwords_whitelist_combination:
                        continue
                    # Just check that text contains all words from combination.
                    #  it must be better to replace with building some "tree" structure from sentence
                    #   (e.g. turn -> off ...)
                    found_combination_words = [stopword
                                               for stopword in stopwords_whitelist_combination
                                               if stopword in not_none_words]
                    if len(found_combination_words) == len(stopwords_whitelist_combination):
                        result.append(word)
        return result

    def matrix(self, text):
        """
        Get text as matrix
        :param text: text
        :type text: str
        :return: matrix
        :rtype: numpy.ndarray
        """
        words = self.split(text)
        vectors = [self.word2vec[word] for word in words]
        return numpy.array(vectors)

    def similarity(self, word1, word2):
        """
        Get similarity of 2 words
        :param word1: word
        :type word1: str
        :param word2: word
        :type word2: str
        :return: words vectors cosine similarity
        :rtype: float
        """
        if word1 not in self.word2vec.vocab or word2 not in self.word2vec.vocab:
            return 0.0
        return self.word2vec.similarity(word1, word2)
