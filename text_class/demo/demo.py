import itertools
import json
import numpy
import gensim
from gensim.models import Word2Vec
from text_class.pynlc.test_data import reuters_classes, word2vec, car_classes, weather_classes
from text_class.pynlc.text_classifier import TextClassifier
from text_class.pynlc.text_processor import TextProcessor
from sklearn.metrics import mean_squared_error


def classification_demo(data_path, train_before, test_before, train_epochs, test_labels_path, instantiated_test_labels_path, trained_path):
    with open(data_path, 'r', encoding='utf-8') as data_source:
        data = json.load(data_source)
    texts = [item["text"] for item in data]
    class_names = [item["classes"] for item in data]
    train_texts = texts[:train_before]
    train_classes = class_names[:train_before]
    test_texts = texts[train_before:test_before]
    test_classes = class_names[train_before:test_before]
    text_processor = TextProcessor("english", [["turn", "on"], ["turn", "off"]], gensim.models.KeyedVectors.load_word2vec_format(word2vec))
    classifier = TextClassifier(text_processor)
    classifier.train(train_texts, train_classes, train_epochs, True)
    prediction = classifier.predict(test_texts)
    with open(test_labels_path, "w", encoding="utf-8") as test_labels_output:
        test_labels_output_lst = []
        for i in range(0, len(prediction)):
            test_labels_output_lst.append({
                "real": test_classes[i],
                "classified": prediction[i]
            })
        json.dump(test_labels_output_lst, test_labels_output)
    instantiated_classifier = TextClassifier(text_processor, **classifier.config)
    instantiated_prediction = instantiated_classifier.predict(test_texts)
    with open(instantiated_test_labels_path, "w", encoding="utf-8") as instantiated_test_labels_output:
        instantiated_test_labels_output_lst = []
        for i in range(0, len(instantiated_prediction)):
            instantiated_test_labels_output_lst.append({
                "real": test_classes[i],
                "classified": instantiated_prediction[i]
            })
        json.dump(instantiated_test_labels_output_lst, instantiated_test_labels_output)
    with open(trained_path, "w", encoding="utf-8") as trained_output:
        json.dump(classifier.config, trained_output, ensure_ascii=True)


def classification_error(files):
    for name in files:
        with open(name, "r", encoding="utf-8") as src:
            data = json.load(src)
        classes = []
        real = []
        for row in data:
            classes.append(row["real"])
            classified = row["classified"]
            row_classes = list(classified.keys())
            row_classes.sort()
            real.append([classified[class_name] for class_name in row_classes])
        labels = []
        class_names = list(set(itertools.chain(*classes)))
        class_names.sort()
        for item_classes in classes:
            labels.append([int(class_name in item_classes) for class_name in class_names])
        real_np = numpy.array(real)
        mse = mean_squared_error(numpy.array(labels), real_np)
        print(name, mse)


if __name__ == '__main__':
    #print("Reuters:\n")
    # classification_demo(reuters_classes, 10000, 15000, 10,
    #                     "reuters_test_labels.json", "reuters_car_test_labels.json",
    #                     "reuters_trained.json")
    # classification_error(["reuters_test_labels.json", "reuters_car_test_labels.json"])
    # print("Car intents:\n")
    # classification_demo(car_classes, 400, 500, 20,
    #                     "car_test_labels.json", "instantiated_car_test_labels.json",
    #                     "car_trained.json")
    # classification_error(["cars_test_labels.json", "instantiated_cars_test_labels.json"])
    print("Weather:\n")
    classification_demo(weather_classes, 40, 50, 30,
                        "weather_test_labels.json", "instantiated_weather_test_labels.json",
                        "weather_trained.json")
    classification_error(["weather_test_labels.json", "instantiated_weather_test_labels.json"])
