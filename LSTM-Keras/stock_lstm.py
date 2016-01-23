'''Train a LSTM on the IMDB sentiment classification task.

The dataset is actually too small for LSTM to be of any advantage
compared to simpler, much faster methods such as TF-IDF+LogReg.

Notes:

- RNNs are tricky. Choice of batch size is important,
choice of loss and optimizer is critical, etc.
Some configurations won't converge.

- LSTM loss decrease patterns during training can be quite different
from what you see with CNNs/MLPs/etc.

GPU command:
    THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python imdb_lstm.py
'''

from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.datasets import imdb
from keras.utils.visualize_util import plot
from math import floor
# import csv
import numpy
import sklearn.cross_validation as crossval

max_features = 5000
maxlen = 20  # cut texts after this number of words (among top max_features most common words)
batch_size = 32

# with open('pkn_d.csv', 'rb') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row['Data'], row['Zamkniecie'])

data = numpy.recfromcsv('dbc_d.csv', delimiter=',')

zamkniecie = data["zamkniecie"]

x_data = numpy.array([zamkniecie[i:i+maxlen] for i in xrange(len(zamkniecie)-maxlen)])
y_data = numpy.array([floor(zamkniecie[i]/zamkniecie[i-1]) for i in xrange(maxlen,len(zamkniecie))])

print (x_data)
print (y_data)



# print('Loading data...')
# (X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features,
#                                                       test_split=0.2)
# print(len(X_train), 'train sequences')
# print(len(X_test), 'test sequences')

X_train, X_test, y_train, y_test = crossval.train_test_split(x_data, y_data, test_size=0.2, random_state=0)

# X_train = numpy.array(x_data[0:len(x_data)*7/10])
# y_train = numpy.array(y_data[0:len(y_data)*7/10])
#
# X_test = numpy.array(x_data[(len(x_data)*7/10):])
# y_test = numpy.array(y_data[(len(y_data)*7/10):])

print (y_train)


print("Pad sequences (samples x time)")
X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)

print('Build model...')
model = Sequential()
model.add(Embedding(max_features, 128, input_length=maxlen))
model.add(LSTM(128))  # try using a GRU instead, for fun
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

# plot(model, to_file='model.png')

# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              class_mode="binary")

#model.load_weights('my_model_dbc_1.h5')


print("Train...")
model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=100,
          validation_data=(X_test, y_test), show_accuracy=True)
score, acc = model.evaluate(X_test, y_test,
                            batch_size=batch_size,
                            show_accuracy=True)


model.save_weights('my_model_dbc_1.h5')

print('Test score:', score)
print('Test accuracy:', acc)
