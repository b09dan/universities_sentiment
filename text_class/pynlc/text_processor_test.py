from unittest import TestCase
from gensim.models import Word2Vec
from .text_processor import TextProcessor
from .test_data import word2vec


class TextProcessorTest(TestCase):
    def testProcessing(self):
        text_processor = TextProcessor("english", [["turn", "on"], ["turn", "off"]],
                                       Word2Vec.load_word2vec_format(word2vec))
        texts = ['Is the forecast calling for snow today?', 'How hot is it today?', 'How much rain will fall today?',
                 'Will it rain?', 'Are we expecting sunny conditions?', 'Will it be dry?', 'Will it be breezy?',
                 'When will the heat subside?', 'Will it be sweltering?', 'Will it be cloudy?']
        splitted = [text_processor.split(text) for text in texts]
        right_splitted = [['forecast', 'calling', 'snow', 'today'], ['hot', 'today'], ['much', 'rain', 'fall', 'today'],
                          ['rain'], ['expecting', 'sunny', 'conditions'], ['dry'], ['breezy'], ['heat', 'subside'],
                          ['sweltering'], ['cloudy']]
        self.assertEqual(splitted, right_splitted)
