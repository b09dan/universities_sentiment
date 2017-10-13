import json

import gensim
from gensim.models import Word2Vec
from text_class.pynlc.test_data import word2vec
from text_class.pynlc import TextProcessor, TextClassifier


if __name__ == '__main__':
    text_processor = TextProcessor("english", [["turn", "on"], ["turn", "off"]],
                                   gensim.models.KeyedVectors.load_word2vec_format(word2vec))
    with open("uni_trained.json", "r", encoding="utf-8") as classifier_data_source:
        classifier_data = json.load(classifier_data_source)
    classifier = TextClassifier(text_processor, **classifier_data)
    texts = [
        "Great university and a very friendly atmosphere!",
        "I would not recommend this university to any, unless there is no other better choice.",
        "Great engineering expertise, nice city, good cooperation with companies in the engineering field, open dialogue and support of student associations."
    ]
    predictions = classifier.predict(texts)
    for i in range(0, len(texts)):
        print(texts[i])
        print(predictions[i])
