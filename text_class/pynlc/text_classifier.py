import copy
import itertools
import numpy
from sklearn.metrics import mean_squared_error
from .classifier import Classifier
from .text_processor import TextProcessor


class TextClassifier:
    """
    Text classifier class
    """
    def __init__(self, text_processor, backend=None, classes=None, backend_extra_args=None):
        """
        Initialize classifier
        :param text_processor: text processor
        :type text_processor: TextProcessor
        :param backend: pretrained network configuration or None
        :type backend: dict|NoneType
        :param classes: class names list (for pretrained classifier) or None
        :type classes: list[str]|NoneType
        :param backend_extra_args: Backend optional arguments. \
          See filter_sizes, nb_filter, hidden_size on Classifier
        :type backend_extra_args: NoneType|dict
        """
        self.backend_extra_args = backend_extra_args
        if backend is not None:
            backend_config = copy.deepcopy(backend)
            if backend_extra_args is not None:
                for key, value in backend_extra_args.items():
                    backend_config[key] = value
            self.backend = Classifier(**backend_config)
        else:
            self.backend = None
        self.text_processor = text_processor
        self.classes = classes

    @property
    def config(self):
        """
        Get configuration dictionary
        :return: config
        :rtype: dict
        """
        return {
            "backend": self.backend.config,
            "classes": self.classes
        }

    def train(self, texts, classes, epochs, verbose=False, validation_split=0.3, callbacks=[]):
        """
        Train on given texts
        :param texts: texts
        :type texts: list[str]
        :param classes: class names (one list for one texts item)
        :type classes: list[list[str]]
        :param epochs: epochs count
        :type epochs: int
        :param verbose: verbose train process?
        :type verbose: bool
        :param validation_split: validation split (0 <= x <= 1)
        :type validation_split: float
        :param callbacks: Train callbacks (e.g. early stopping)
        """
        self.classes = list(set(itertools.chain(*classes)))
        self.classes.sort()
        matrixes = [self.text_processor.matrix(text)
                    for text in texts]
        vector_count = 2 * max([len(item) for item in matrixes])
        vector_size = matrixes[0].shape[1]
        labels = numpy.array([[int(class_name in text_classes) for class_name in self.classes]
                              for text_classes in classes])
        backend_config = {}
        if self.backend_extra_args is not None:
            for key, value in self.backend_extra_args.items():
                backend_config[key] = value
        self.backend = Classifier(vector_count, vector_size, len(self.classes), **backend_config)
        self.backend.train(matrixes, labels, epochs, verbose,
                           validation_split=validation_split, callbacks=callbacks)

    def predict(self, texts):
        """
        Predict classes
        :param texts: texts
        :type texts: list[str]
        :return: classification results (one per one texts item)
        :rtype: list[dict[str, float]]
        """
        matrixes = [self.text_processor.matrix(text)
                    for text in texts]
        labels = self.backend.predict(matrixes)
        result = []
        for row in labels:
            data = {}
            for i, class_name in enumerate(self.classes):
                data[class_name] = float(row[i])
            result.append(data)
        return result

    def error(self, texts, right_classes):
        """
        Calculate classification error
        :param texts: texts
        :type texts: list[str]
        :param right_classes: classes
        :type right_classes: list[list[str]]
        :return: error
        :rtype: float
        """
        prediction = self.predict(texts)
        right_values = [[int(class_name in item_classes) for class_name in self.classes]
                        for item_classes in right_classes]
        values = [[item_classes[class_name] for class_name in self.classes]
                  for item_classes in prediction]
        return mean_squared_error(numpy.array(right_values), numpy.array(values))
