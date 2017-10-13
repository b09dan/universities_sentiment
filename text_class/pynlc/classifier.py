import keras.layers
from keras.models import Sequential, Model
from keras.layers import Convolution1D, MaxPooling1D, Dense, Dropout, Input, Flatten, Merge
from keras.optimizers import RMSprop
import numpy


class Classifier:
    """
    Classifier CNN wrapper.
    """
    def __init__(self, vector_count, vector_size, output_count, model=None, weights=None,
                 filter_sizes=[1, 2], nb_filter=150, hidden_size=200):
        """
        Classifier network
        :param vector_count: maximal input vector count
        :type vector_count: int
        :param vector_size: word vector size
        :type vector_size: int
        :param output_count: outputs count
        :type output_count: int
        :param model: pretrained model or None
        :type model: NoneType|dict
        :param weights: pretrained model weights
        :type weights: NoneType|dict
        :param filter_sizes: conv1d filter size
        :type filter_sizes: list[int]
        :param nb_filter: nv_filter for conv1d
        :type nb_filter: int
        :param hidden_size: hidden layer size
        :type hidden_size: int
        """
        self.vector_count = vector_count
        self.vector_size = vector_size
        self.output_count = output_count
        self.filter_sizes = filter_sizes
        self.nb_filter = nb_filter
        self.hidden_size = hidden_size
        if model is None:
            self.model = self._build_model(output_count)
        else:
            self.model = Sequential.from_config(model)
        optimizer = RMSprop(lr=0.0005, epsilon=1e-10)
        self.model.compile(optimizer, 'binary_crossentropy', metrics=['accuracy'])
        if weights is not None:
            self.model.set_weights([numpy.array(layer_weights) for layer_weights in weights])

    def _build_model(self, output_count):
        input = Input(shape=(self.vector_count, self.vector_size,))
        convs = []
        for filter_size in self.filter_sizes:
            conv = Convolution1D(nb_filter=self.nb_filter,
                                 filter_length=filter_size,
                                 border_mode='valid',
                                 activation='relu',
                                 subsample_length=1)(input)
            pool = MaxPooling1D(pool_size=2)(conv)
            flatten = Flatten()(pool)
            convs.append(flatten)
        if len(convs) > 1:
            out = keras.layers.concatenate(convs)
        else:
            out = convs[0]
        graph = Model(input=input, output=out)
        model = Sequential()
        model.add(Dropout(0.25, input_shape=(self.vector_count, self.vector_size,)))
        model.add(graph)
        model.add(Dense(self.hidden_size))
        model.add(Dropout(0.25))
        model.add(Dense(output_count, activation='sigmoid'))
        return model

    def fit_matrixes(self, matrices):
        """
        Fit matrices to given vector count
        :param matrices: input
        :type matrices: numpy.ndarray
        :return: resized
        :rtype: numpy.ndarray
        """
        resized = [numpy.resize(matrix, (self.vector_count, self.vector_size,))
                   for matrix in matrices]
        return numpy.array(resized)

    def train(self, matrices, labels, epochs, verbose=False, validation_split=0.3, callbacks=[]):
        """
        Train network on given examples
        :param matrices: input sentence matrices
        :type matrices: numpy.ndarray
        :param labels: input labels
        :type labels: numpy.ndarray
        :param epochs: epoch count
        :type epochs: int
        :param verbose: verbose train process?
        :type verbose: bool
        :param validation_split: validation split (0 <= x <= 1)
        :type validation_split: float
        :param callbacks: Keras callbacks (e.g. early stopping)
        """
        features = self.fit_matrixes(matrices)
        self.model.fit(features, labels, epochs=epochs, verbose=verbose, batch_size=20,
                       validation_split=validation_split, callbacks=callbacks)

    def predict(self, matrices):
        """
        Make prediction
        :param matrices: input sentence matrices
        :type matrices: numpy.ndarray
        :return: predicted classes
        :rtype: numpy.ndarray
        """
        features = self.fit_matrixes(matrices)
        return self.model.predict(features)

    @property
    def config(self):
        """
        Get configuration dictionary
        :return: config
        :rtype: dict
        """
        return {
            'vector_count': self.vector_count,
            'vector_size': self.vector_size,
            'output_count': self.output_count,
            'model': self.model.get_config(),
            'weights': [layer_weight.tolist() for layer_weight in self.model.get_weights()],
            'filter_sizes': self.filter_sizes,
            'nb_filter': self.nb_filter,
            'hidden_size': self.hidden_size,
        }
