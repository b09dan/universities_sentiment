import json
from unittest import TestCase
from gensim.models import Word2Vec
from .text_classifier import TextClassifier
from .text_processor import TextProcessor
from .test_data import word2vec, weather_classes, car_classes


class TextClassifierTest(TestCase):
    def _classifier(self, classes, train_before, backend_extra_args):
        text_processor = TextProcessor("english", [["turn", "on"], ["turn", "off"]],
                                       Word2Vec.load_word2vec_format(word2vec))
        with open(classes, "r", encoding="utf-8") as weather_file:
            weather = json.load(weather_file)
        texts = [item["text"] for item in weather]
        class_names = [item["classes"] for item in weather]
        classifier = TextClassifier(text_processor, backend_extra_args=backend_extra_args)
        classifier.train(texts[:train_before], class_names[:train_before], 25, verbose=True)
        return classifier, texts, class_names

    def testWeatherClassification(self):
        classifier, texts, class_names = self._classifier(weather_classes, 40, {
            'filter_sizes': [1],
            'nb_filter': 100,
            'hidden_size': 20
        })
        error = classifier.error(texts[40:], class_names[40:])
        self.assertTrue(error <= 0.1)

    def testWeatherFalsePositive(self):
        classifier, texts, class_names = self._classifier(weather_classes, 40, {
            'filter_sizes': [1],
            'nb_filter': 100,
            'hidden_size': 4
        })
        false_positive_test_text = 'So what is meaning of natural language classification?'
        false_positive_test_prediction = classifier.predict([false_positive_test_text])[0]
        self.assertTrue(false_positive_test_prediction['temperature'] < 0.8)
        self.assertTrue(false_positive_test_prediction['conditions'] < 0.8)

    def testCarClassification(self):
        classifier, texts, class_names = self._classifier(car_classes, 350, {
            'filter_sizes': [1, 2],
            'nb_filter': 150,
            'hidden_size': 200
        })
        error = classifier.error(texts[350:], class_names[350:])
        self.assertTrue(error <= 0.1)

    def testCarFalsePositive(self):
        classifier, texts, class_names = self._classifier(car_classes, 350, {
            'filter_sizes': [1, 2],
            'nb_filter': 150,
            'hidden_size': 50
        })
        false_positive_test_text = 'So what is meaning of natural language classification?'
        false_positive_test_prediction = classifier.predict([false_positive_test_text])[0]
        self.assertTrue(false_positive_test_prediction['capabilities'] < 0.8)
        self.assertTrue(false_positive_test_prediction['turn_up'] < 0.8)
        self.assertTrue(false_positive_test_prediction['phone'] < 0.8)
        self.assertTrue(false_positive_test_prediction['weather'] < 0.8)
        self.assertTrue(false_positive_test_prediction['goodbyes'] < 0.8)
        self.assertTrue(false_positive_test_prediction['turn_off'] < 0.8)
        self.assertTrue(false_positive_test_prediction['turn_down'] < 0.8)
        self.assertTrue(false_positive_test_prediction['not_specified'] < 0.8)
        self.assertTrue(false_positive_test_prediction['locate_amenity'] < 0.8)
        self.assertTrue(false_positive_test_prediction['greetings'] < 0.8)
        self.assertTrue(false_positive_test_prediction['out_of_scope'] < 0.8)
        self.assertTrue(false_positive_test_prediction['traffic_update'] < 0.8)

