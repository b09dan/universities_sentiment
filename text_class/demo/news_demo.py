import json

import gensim
from gensim.models import Word2Vec
from text_class.pynlc.test_data import word2vec
from text_class.pynlc import TextProcessor, TextClassifier


if __name__ == '__main__':
    text_processor = TextProcessor("english", [["turn", "on"], ["turn", "off"]],
                                   gensim.models.KeyedVectors.load_word2vec_format(word2vec))
    with open("news_trained.json", "r", encoding="utf-8") as classifier_data_source:
        classifier_data = json.load(classifier_data_source)
    classifier = TextClassifier(text_processor, **classifier_data)
    texts = [
        "Alcoa, less than a month away from splitting itself in two, reported worse-than-expected earnings growth in the latest quarter as lower alumina pricing and changes to aerospace delivery schedules dented revenue.\u00a0Continue Reading Below Shares fell 6.2% to $29.50 in premarket trading.\u00a0 The company is splitting its raw-aluminum operations, which will keep the Alcoa name, from the firm that will house the companys faster-growing businesses supplying the aerospace and automotive markets, called Arconic. The split is slated for Nov. 1. Klaus Kleinfeld, now chief executive of Alcoa, will be CEO of Arconic.\u00a0 The New York-based aluminum maker, by tradition the first major U.S. company to report its third-quarter results, again broke down its overall results as they are expected to appear after the split.\u00a0 At the units that will form Arconic, revenue fell 1% from a year earlier to $3.4 billion, reflecting adjustments to delivery schedules in the aerospace industry and softness in North America commercial transportation and pricing pressures.\u00a0 Alcoas traditional metals operations -- which include smelting, mining and refining -- reported revenue of $2.3 billion, which it said was roughly the same as the year-ago quarter, reflecting continued low alumina prices and the impact of curtailed and closed operations.\u00a0Continue Reading BelowADVERTISEMENT Over all, Alcoa reported a profit of $166 million, or 33 cents a share, compared with $44 million, or 6 cents a share, a year ago. Excluding certain items, the company earned 32 cents a share, up from 21 cents a year ago. Analysts polled by Thomson Reuters expected 35 cents a share.\u00a0 Revenue fell 6% to $5.21 billion, below analysts projections of $5.31 billion.\u00a0 Alcoas raw aluminum business has been hammered this decade by an oversupply of aluminum generated largely by China that has caused prices on the London Metal Exchange to fall to around $1,600 a ton, down from around $2,500 a ton five years ago. To cope with weak prices, Alcoa has been closing high-cost smelters in the U.S.\u00a0 The earnings report Tuesday was slated to be Alcoas last as a single firm"
    ]
    predictions = classifier.predict(texts)
    for i in range(0, len(texts)):
        print(texts[i])
        print(predictions[i])
